########################################################################################################
# The RWKV Language Model - https://github.com/BlinkDL/RWKV-LM
########################################################################################################

import types, gc, os, time
import torch
from torch.nn import functional as F
torch.backends.cudnn.benchmark = True
torch.backends.cudnn.allow_tf32 = True
torch.backends.cuda.matmul.allow_tf32 = True
current_path = os.path.dirname(os.path.abspath(__file__))

########################################################################################################

if os.environ.get('RWKV_JIT_ON') != '0':
    os.environ["RWKV_JIT_ON"] = '1'
    MyModule = torch.jit.ScriptModule
    MyFunction = torch.jit.script_method
else:
    MyModule = torch.nn.Module
    def __nop(ob):
        return ob
    MyFunction = __nop

if os.environ.get('RWKV_CUDA_ON') == '1':
    from torch.utils.cpp_extension import load
    wkv_cuda = load(name=f"wkv_cuda", sources=[f"{current_path}/cuda/wkv_op.cpp", f"{current_path}/cuda/wkv_cuda.cu"], verbose=True, extra_cuda_cflags=["-t 4", "-std=c++17", "--use_fast_math", "-O3", "--extra-device-vectorization"])
    class WKV(torch.autograd.Function): # only for fp16
        @staticmethod
        def forward(ctx, T, C, w, u, k, v, aa, bb, pp):
            assert 1 * C % min(C, 32) == 0
            assert k.dtype == torch.float16
            w = w.contiguous()
            u = u.contiguous()
            k = k.contiguous()
            v = v.contiguous()
            y = torch.empty((T, C), device=w.device, memory_format=torch.contiguous_format, dtype=torch.float16)
            wkv_cuda.forward(1, T, C, w, u, k, v, y, aa, bb, pp)
            return y, aa, bb, pp
    def RUN_CUDA(T, C, w, u, k, v, aa, bb, pp):
        return WKV.apply(T, C, w, u, k, v, aa, bb, pp)
else:
    os.environ["RWKV_CUDA_ON"] = '0'

########################################################################################################

class RWKV(MyModule):
    def __init__(self, model, strategy):
        super().__init__()
        self.args = types.SimpleNamespace()
        args = self.args
        args.MODEL_NAME = model
        args.strategy_string = strategy

        # Rescale for fp16 mode: set x = x/2 every X layer (to avoid overflow)
        self.RESCALE_LAYER = 6 if 'fp16' in strategy else 0
        print(f'RWKV_JIT_ON {os.environ["RWKV_JIT_ON"]} RWKV_CUDA_ON {os.environ["RWKV_CUDA_ON"]} RESCALE_LAYER {self.RESCALE_LAYER}\n')

        # We will load model to CPU first
        args.MODEL_NAME = args.MODEL_NAME.strip()
        if not args.MODEL_NAME.endswith('.pth'):
            args.MODEL_NAME += '.pth'
        print(f'Loading {args.MODEL_NAME} ...')
        with torch.no_grad():
            self.w = torch.load(args.MODEL_NAME, map_location='cpu')
            gc.collect()
            w = self.w
            args.n_embd = w['emb.weight'].shape[1]
            try: # precompute embedding
                w['emb.weight'] = F.layer_norm(w['emb.weight'], (args.n_embd,), weight=w['blocks.0.ln0.weight'], bias=w['blocks.0.ln0.bias'])
            except:
                w['emb.weight'] = F.layer_norm(w['emb.weight'].float(), (args.n_embd,), weight=w['blocks.0.ln0.weight'].float(), bias=w['blocks.0.ln0.bias'].float())
            del w['blocks.0.ln0.weight']
            del w['blocks.0.ln0.bias']

            keys = list(w.keys())
            args.n_layer = 0
            for x in keys:
                layer_id = int(x.split('.')[1]) if ('blocks.' in x) else 0
                args.n_layer = max(args.n_layer, layer_id+1)

            # Compute strategy
            s = [x.strip().split(' ') for x in strategy.split('->')]
            plan = [0] * len(s)
            stream_i = -1
            stream_count = 0
            to_allocate = args.n_layer + 1
            allocated = 0
            free_slots = 0
            for i in range(len(s)):
                si = s[i]
                si1 = si[1]
                if si1.startswith('fp32'): si[1] = [torch.float]
                elif si1.startswith('fp16'): si[1] = [torch.float16]
                elif si1.startswith('bf16'): si[1] = [torch.bfloat16]
                if si1.endswith('i8'): si[1] += [torch.uint8]
                else: si[1] += [si[1][0]]
                if len(si) > 2:
                    ss = si[2]
                    assert ss.startswith('*')
                    if ss.endswith('+'):
                        plan[i] = int(ss[1:-1])
                        stream_i = i
                    else:
                        plan[i] = int(ss[1:])
                    allocated += plan[i]
                    if allocated >= to_allocate:
                        plan[i] += to_allocate - allocated
                        break
                else:
                    free_slots += 1
            if stream_i < 0:
                if free_slots > 0 and to_allocate > allocated:
                    for i in range(len(s)):
                        if plan[i] == 0:
                            plan[i] = (to_allocate - allocated) // free_slots
                            allocated += plan[i]
                            free_slots -= 1
                if to_allocate > allocated:
                    plan[len(s)-1] += to_allocate - allocated
            else:
                if to_allocate > allocated:
                    stream_count = to_allocate - allocated
                    plan[stream_i] += stream_count
            print(f'Strategy: (total {args.n_layer}+1={args.n_layer+1} layers)')
            for i in range(len(s)):
                ss = s[i]
                if i != stream_i:
                    print(f'* {ss[0]} {str(ss[1]).replace("torch.","")}, store {plan[i]} layers')
                else:
                    print(f'* {ss[0]} {str(ss[1]).replace("torch.","")}, store {plan[i]-stream_count} layers, stream {stream_count} layers')
                plan[i] += (0 if i == 0 else plan[i-1])
            self.strategy = [None] * (args.n_layer + 1)
            strategy = self.strategy
            for n in range(args.n_layer + 1):
                for i in range(len(s)):
                    if n < plan[i]:
                        strategy[n] = types.SimpleNamespace()
                        strategy[n].device = s[i][0]
                        strategy[n].atype = s[i][1][0]
                        strategy[n].wtype = s[i][1][1]
                        strategy[n].stream = False
                        if i == stream_i and n >= (plan[i] - stream_count):
                            strategy[n].stream = True
                        break
                print(f"{n}-{strategy[n].device}-{str(strategy[n].atype).replace('torch.','')}-{str(strategy[n].wtype).replace('torch.','')}{'-stream' if strategy[n].stream else ''}",end=' ')
            print()

            # Load weights
            print_need_newline = False
            for x in keys:
                w[x].requires_grad = False
                layer_id = int(x.split('.')[1]) if ('blocks.' in x) else 0
                if ('ln_out.' in x) or ('head.' in x):
                    layer_id = args.n_layer
                dd = strategy[layer_id]
                DEVICE = dd.device
                ATYPE = dd.atype
                WTYPE = dd.wtype

                if self.RESCALE_LAYER > 0:
                    if 'att.output.weight' in x:
                        w[x] = w[x] / (2 ** int(layer_id // self.RESCALE_LAYER))
                    if 'ffn.value.weight' in x:
                        w[x] = w[x] / (2 ** int(layer_id // self.RESCALE_LAYER))

                if '.time_' in x:
                    w[x] = w[x].squeeze()
                if 'key.weight' in x or 'value.weight' in x or 'receptance.weight' in x or 'output.weight' in x or 'head.weight' in x:
                    w[x] = w[x].t()
                
                if '.time_decay' in x: # need fp32 for this
                    w[x] = -torch.exp(w[x].float())
                elif '.time_first' in x: # need fp32 for this
                    w[x] = w[x].float()
                else:
                    if (len(w[x].shape) == 2) and ('emb' not in x):
                        if WTYPE != torch.uint8:
                            w[x] = w[x].to(dtype=WTYPE)
                        else:
                            w[x] = w[x].float()

                            if w[x].shape[0] > w[x].shape[1]:
                                w[x+'_my'] = torch.amin(w[x], dim=1).unsqueeze(1)
                                w[x] = w[x] - w[x+'_my']
                                w[x+'_mx'] = torch.amin(w[x], dim=0)
                                w[x] = w[x] - w[x+'_mx']
                                w[x+'_rx'] = torch.amax(w[x], dim=0)
                                w[x] = w[x] / w[x+'_rx']
                                w[x+'_ry'] = torch.amax(w[x], dim=1).unsqueeze(1)
                                w[x] = w[x] / w[x+'_ry']
                            else:
                                w[x+'_mx'] = torch.amin(w[x], dim=0)
                                w[x] = w[x] - w[x+'_mx']
                                w[x+'_my'] = torch.amin(w[x], dim=1).unsqueeze(1)
                                w[x] = w[x] - w[x+'_my']
                                w[x+'_rx'] = torch.amax(w[x], dim=0)
                                w[x] = w[x] / w[x+'_rx']
                                w[x+'_ry'] = torch.amax(w[x], dim=1).unsqueeze(1)
                                w[x] = w[x] / w[x+'_ry']

                            w[x] = torch.clip(torch.floor(w[x] * 256), min=0, max=255).to(dtype=torch.uint8)
                            w[x+'_mx'] = w[x+'_mx'].to(dtype=ATYPE).contiguous()
                            w[x+'_rx'] = (w[x+'_rx'] / 16).to(dtype=ATYPE).contiguous()
                            w[x+'_my'] = w[x+'_my'].to(dtype=ATYPE).contiguous()
                            w[x+'_ry'] = (w[x+'_ry'] / 16).to(dtype=ATYPE).contiguous()
                    else:
                        w[x] = w[x].to(dtype=ATYPE)
                
                if 'emb.' in x:
                    w[x] = w[x].contiguous()
                elif (dd.stream) and (x.endswith('key.weight') or x.endswith('value.weight') or x.endswith('receptance.weight') or x.endswith('output.weight')):
                    try:
                        w[x] = w[x].contiguous().pin_memory() # if you see "CUDA error: out of memory" here, that's out of CPU RAM, not VRAM. Get more RAM :)
                    except:
                        print('Note: You are running out of RAM. Get more CPU RAM. Now this will run much slower.')
                elif DEVICE != 'cpu':
                    w[x] = w[x].to(device=DEVICE).contiguous()
                else:
                    w[x] = w[x].contiguous()
                
                if (dd.stream) or (DEVICE != 'cpu'):
                    try:
                        w[x+'_mx'] = w[x+'_mx'].to(device=DEVICE).contiguous()
                        w[x+'_rx'] = w[x+'_rx'].to(device=DEVICE).contiguous()
                        w[x+'_my'] = w[x+'_my'].to(device=DEVICE).contiguous()
                        w[x+'_ry'] = w[x+'_ry'].to(device=DEVICE).contiguous()
                    except:
                        pass

                if 'ffn.value.weight' in x:
                    gc.collect()
                    if 'cuda' in args.strategy_string:
                        torch.cuda.empty_cache()

                shape = [i for i in w[x].shape if i != 1]
                if len(shape) > 1:
                    shape = f" {str(shape[0]).rjust(5)} {str(shape[1]).rjust(5)}"
                else:
                    shape = f" {str(shape[0]).rjust(5)}      "
                if layer_id == 0 or layer_id >= args.n_layer-1:
                    if print_need_newline:
                        print('\n', end = '')
                        print_need_newline = False
                    dt = str(w[x].dtype).replace('torch.', '')
                    dt = dt.replace('float32', 'f32').replace('bfloat16', 'bf16').replace('float16', 'f16').replace('uint8', 'i8')
                    print(x.ljust(32), dt.rjust(4), str(w[x].device).rjust(8), shape, ' (pinned)' if w[x].is_pinned() else '')
                else:
                    print_need_newline = True
                    print('.', end = '', flush = True)
            assert len(keys) == 4 + (4+9+5) * args.n_layer, 'Error: not a RWKV-4 model (4a and 4b models are not supported as of now)'
            gc.collect()
            if 'cuda' in args.strategy_string:
                torch.cuda.empty_cache()

    @MyFunction
    def mm8_seq(self, x, w, mx, rx, my, ry):
        return x @ ((w.to(dtype=x.dtype) + 0.5) * ry * rx + my + mx)
    
    @MyFunction
    def mm8_one(self, x, w, mx, rx, my, ry):
        return x @ ((w.to(dtype=x.dtype) + 0.5) * ry * rx + my + mx)

    ########################################################################################################

    @MyFunction
    def ffn_one(self, x, sx, ln_w, ln_b, k_mix, r_mix, kw, vw, rw, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry):
        xx = F.layer_norm(x, (x.shape[-1],), weight=ln_w, bias=ln_b)
        kx = xx * k_mix + sx * (1 - k_mix)
        rx = xx * r_mix + sx * (1 - r_mix)

        r = torch.sigmoid(rx @ rw)
        vx = torch.square(torch.relu(kx @ kw))
        out = r * (vx @ vw)
        return x + out, xx

    @MyFunction
    def ffn_one_i8(self, x, sx, ln_w, ln_b, k_mix, r_mix, kw, vw, rw, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry):
        xx = F.layer_norm(x, (x.shape[-1],), weight=ln_w, bias=ln_b)
        kx = xx * k_mix + sx * (1 - k_mix)
        rx = xx * r_mix + sx * (1 - r_mix)

        r = torch.sigmoid(self.mm8_one(rx, rw, rmx, rrx, rmy, rry))
        vx = torch.square(torch.relu(self.mm8_one(kx, kw, kmx, krx, kmy, kry)))
        out = r * (self.mm8_one(vx, vw, vmx, vrx, vmy, vry))
        return x + out, xx
    
    ########################################################################################################

    @MyFunction
    def ffn_seq(self, x, sx, ln_w, ln_b, k_mix, r_mix, kw, vw, rw, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry):
        xx = F.layer_norm(x, (x.shape[-1],), weight=ln_w, bias=ln_b)
        sx = torch.cat((sx.unsqueeze(0), xx[:-1,:]))
        kx = xx * k_mix + sx * (1 - k_mix)
        rx = xx * r_mix + sx * (1 - r_mix)

        r = torch.sigmoid(rx @ rw)
        vx = torch.square(torch.relu(kx @ kw))
        out = r * (vx @ vw)
        return x + out, xx[-1,:]

    @MyFunction
    def ffn_seq_i8(self, x, sx, ln_w, ln_b, k_mix, r_mix, kw, vw, rw, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry):
        xx = F.layer_norm(x, (x.shape[-1],), weight=ln_w, bias=ln_b)
        sx = torch.cat((sx.unsqueeze(0), xx[:-1,:]))
        kx = xx * k_mix + sx * (1 - k_mix)
        rx = xx * r_mix + sx * (1 - r_mix)

        r = torch.sigmoid(self.mm8_seq(rx, rw, rmx, rrx, rmy, rry))
        vx = torch.square(torch.relu(self.mm8_seq(kx, kw, kmx, krx, kmy, kry)))
        out = r * (self.mm8_seq(vx, vw, vmx, vrx, vmy, vry))
        return x + out, xx[-1,:]

    ########################################################################################################

    @MyFunction
    def att_one(self, x, sx, aa, bb, pp, ln_w, ln_b, k_mix, v_mix, r_mix, t_decay, t_first, kw, vw, rw, ow, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry, omx, orx, omy, ory):
        xx = F.layer_norm(x, (x.shape[-1],), weight=ln_w, bias=ln_b)
        kx = xx * k_mix + sx * (1 - k_mix)
        vx = xx * v_mix + sx * (1 - v_mix)
        rx = xx * r_mix + sx * (1 - r_mix)

        r = torch.sigmoid(rx @ rw)
        k = (kx @ kw).float()
        v = (vx @ vw).float()

        ww = t_first + k
        p = torch.maximum(pp, ww)
        e1 = torch.exp(pp - p)
        e2 = torch.exp(ww - p)
        wkv = ((e1 * aa + e2 * v) / (e1 * bb + e2)).to(dtype=x.dtype)
        ww = t_decay + pp
        p = torch.maximum(ww, k)
        e1 = torch.exp(ww - p)
        e2 = torch.exp(k - p)

        out = (r * wkv) @ ow
        return x + out, xx, e1 * aa + e2 * v, e1 * bb + e2, p

    @MyFunction
    def att_one_i8(self, x, sx, aa, bb, pp, ln_w, ln_b, k_mix, v_mix, r_mix, t_decay, t_first, kw, vw, rw, ow, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry, omx, orx, omy, ory):
        xx = F.layer_norm(x, (x.shape[-1],), weight=ln_w, bias=ln_b)
        kx = xx * k_mix + sx * (1 - k_mix)
        vx = xx * v_mix + sx * (1 - v_mix)
        rx = xx * r_mix + sx * (1 - r_mix)

        r = torch.sigmoid(self.mm8_one(rx, rw, rmx, rrx, rmy, rry))
        k = (self.mm8_one(kx, kw, kmx, krx, kmy, kry)).float()
        v = (self.mm8_one(vx, vw, vmx, vrx, vmy, vry)).float()

        ww = t_first + k
        p = torch.maximum(pp, ww)
        e1 = torch.exp(pp - p)
        e2 = torch.exp(ww - p)
        wkv = ((e1 * aa + e2 * v) / (e1 * bb + e2)).to(dtype=x.dtype)
        ww = t_decay + pp
        p = torch.maximum(ww, k)
        e1 = torch.exp(ww - p)
        e2 = torch.exp(k - p)

        out = self.mm8_one(r * wkv, ow, omx, orx, omy, ory)
        return x + out, xx, e1 * aa + e2 * v, e1 * bb + e2, p

    ########################################################################################################

    @MyFunction
    def att_seq(self, x, sx, aa, bb, pp, ln_w, ln_b, k_mix, v_mix, r_mix, t_decay, t_first, kw, vw, rw, ow, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry, omx, orx, omy, ory):
        xx = F.layer_norm(x, (x.shape[-1],), weight=ln_w, bias=ln_b)
        sx = torch.cat((sx.unsqueeze(0), xx[:-1,:]))
        kx = xx * k_mix + sx * (1 - k_mix)
        vx = xx * v_mix + sx * (1 - v_mix)
        rx = xx * r_mix + sx * (1 - r_mix)

        r = torch.sigmoid(rx @ rw)
        k = (kx @ kw).float()
        v = (vx @ vw).float()

        T = x.shape[0]
        for t in range(T):
            kk = k[t]
            vv = v[t]
            ww = t_first + kk
            p = torch.maximum(pp, ww)
            e1 = torch.exp(pp - p)
            e2 = torch.exp(ww - p)
            sx[t] = ((e1 * aa + e2 * vv) / (e1 * bb + e2)).to(dtype=x.dtype)
            ww = t_decay + pp
            p = torch.maximum(ww, kk)
            e1 = torch.exp(ww - p)
            e2 = torch.exp(kk - p)
            aa = e1 * aa + e2 * vv
            bb = e1 * bb + e2
            pp = p
        out = (r * sx) @ ow
        return x + out, xx[-1,:], aa, bb, pp

    @MyFunction
    def att_seq_i8(self, x, sx, aa, bb, pp, ln_w, ln_b, k_mix, v_mix, r_mix, t_decay, t_first, kw, vw, rw, ow, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry, omx, orx, omy, ory):
        xx = F.layer_norm(x, (x.shape[-1],), weight=ln_w, bias=ln_b)
        sx = torch.cat((sx.unsqueeze(0), xx[:-1,:]))
        kx = xx * k_mix + sx * (1 - k_mix)
        vx = xx * v_mix + sx * (1 - v_mix)
        rx = xx * r_mix + sx * (1 - r_mix)

        r = torch.sigmoid(self.mm8_seq(rx, rw, rmx, rrx, rmy, rry))
        k = self.mm8_seq(kx, kw, kmx, krx, kmy, kry).float()
        v = self.mm8_seq(vx, vw, vmx, vrx, vmy, vry).float()

        T = x.shape[0]
        for t in range(T):
            kk = k[t]
            vv = v[t]
            ww = t_first + kk
            p = torch.maximum(pp, ww)
            e1 = torch.exp(pp - p)
            e2 = torch.exp(ww - p)
            sx[t] = ((e1 * aa + e2 * vv) / (e1 * bb + e2)).to(dtype=x.dtype)
            ww = t_decay + pp
            p = torch.maximum(ww, kk)
            e1 = torch.exp(ww - p)
            e2 = torch.exp(kk - p)
            aa = e1 * aa + e2 * vv
            bb = e1 * bb + e2
            pp = p
        out = self.mm8_seq(r * sx, ow, omx, orx, omy, ory)
        return x + out, xx[-1,:], aa, bb, pp

    ########################################################################################################
    
    @MyFunction
    def cuda_att_seq_pre(self, x, sx, ln_w, ln_b, k_mix, v_mix, r_mix, kw, vw, rw):
        T, C = x.size()
        xx = F.layer_norm(x, (C,), weight=ln_w, bias=ln_b)
        sx = torch.cat((sx.unsqueeze(0), xx[:-1,:]))
        kx = xx * k_mix + sx * (1 - k_mix)
        vx = xx * v_mix + sx * (1 - v_mix)
        rx = xx * r_mix + sx * (1 - r_mix)
        r = torch.sigmoid(rx @ rw)
        k = kx @ kw
        v = vx @ vw
        return xx[-1,:], r, k, v
    @MyFunction
    def cuda_att_seq_post(self, x, r, y, ow):
        out = (r * y) @ ow
        return x + out
    def cuda_att_seq(self, x, sx, aa, bb, pp, ln_w, ln_b, k_mix, v_mix, r_mix, t_decay, t_first, kw, vw, rw, ow, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry, omx, orx, omy, ory):
        T, C = x.size()
        xx, r, k, v = self.cuda_att_seq_pre(x, sx, ln_w, ln_b, k_mix, v_mix, r_mix, kw, vw, rw)
        y, aa, bb, pp = RUN_CUDA(T, C, t_decay, t_first, k, v, aa, bb, pp)
        out = self.cuda_att_seq_post(x, r, y, ow)
        return out, xx, aa, bb, pp

    @MyFunction
    def cuda_att_seq_pre_i8(self, x, sx, ln_w, ln_b, k_mix, v_mix, r_mix, kw, vw, rw, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry):
        T, C = x.size()
        xx = F.layer_norm(x, (C,), weight=ln_w, bias=ln_b)
        sx = torch.cat((sx.unsqueeze(0), xx[:-1,:]))
        kx = xx * k_mix + sx * (1 - k_mix)
        vx = xx * v_mix + sx * (1 - v_mix)
        rx = xx * r_mix + sx * (1 - r_mix)
        r = torch.sigmoid(self.mm8_seq(rx, rw, rmx, rrx, rmy, rry))
        k = self.mm8_seq(kx, kw, kmx, krx, kmy, kry)
        v = self.mm8_seq(vx, vw, vmx, vrx, vmy, vry)
        return xx[-1,:], r, k, v
    @MyFunction
    def cuda_att_seq_post_i8(self, x, r, y, ow, omx, orx, omy, ory):
        out = self.mm8_seq(r * y, ow, omx, orx, omy, ory)
        return x + out
    def cuda_att_seq_i8(self, x, sx, aa, bb, pp, ln_w, ln_b, k_mix, v_mix, r_mix, t_decay, t_first, kw, vw, rw, ow, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry, omx, orx, omy, ory):
        T, C = x.size()
        xx, r, k, v = self.cuda_att_seq_pre_i8(x, sx, ln_w, ln_b, k_mix, v_mix, r_mix, kw, vw, rw, kmx, krx, kmy, kry, vmx, vrx, vmy, vry, rmx, rrx, rmy, rry)
        y, aa, bb, pp = RUN_CUDA(T, C, t_decay, t_first, k, v, aa, bb, pp)
        out = self.cuda_att_seq_post_i8(x, r, y, ow, omx, orx, omy, ory)
        return out, xx, aa, bb, pp

    ########################################################################################################

    def forward(self, tokens, state, full_output=False):
        with torch.no_grad():
            w = self.w
            args = self.args

            if state == None:
                state = [None] * args.n_layer * 5
                for i in range(args.n_layer): # state: 0=att_xx 1=att_aa 2=att_bb 3=att_pp 4=ffn_xx
                    dd = self.strategy[i]
                    dev = dd.device
                    atype = dd.atype
                    state[i*5+0] = torch.zeros(args.n_embd, dtype=atype, requires_grad=False, device=dev).contiguous()
                    state[i*5+1] = torch.zeros(args.n_embd, dtype=torch.float, requires_grad=False, device=dev).contiguous()
                    state[i*5+2] = torch.zeros(args.n_embd, dtype=torch.float, requires_grad=False, device=dev).contiguous()
                    state[i*5+3] = torch.zeros(args.n_embd, dtype=torch.float, requires_grad=False, device=dev).contiguous() - 1e30
                    state[i*5+4] = torch.zeros(args.n_embd, dtype=atype, requires_grad=False, device=dev).contiguous()

            seq_mode = len(tokens) > 1

            x = w['emb.weight'][tokens if seq_mode else tokens[0]]

            for i in range(args.n_layer):
                bbb = f'blocks.{i}.'
                att = f'blocks.{i}.att.'
                ffn = f'blocks.{i}.ffn.'
                dd = self.strategy[i]
                dev = dd.device
                atype = dd.atype
                wtype = dd.wtype
                if seq_mode:
                    if 'cuda' in str(dev) and os.environ["RWKV_CUDA_ON"] == '1':
                        ATT = self.cuda_att_seq if wtype != torch.uint8 else self.cuda_att_seq_i8
                    else:
                        ATT = self.att_seq if wtype != torch.uint8 else self.att_seq_i8
                    FFN = self.ffn_seq if wtype != torch.uint8 else self.ffn_seq_i8
                else:
                    ATT = self.att_one if wtype != torch.uint8 else self.att_one_i8
                    FFN = self.ffn_one if wtype != torch.uint8 else self.ffn_one_i8

                x = x.to(dtype=atype, device=dev)

                kw = w[f'{att}key.weight']
                vw = w[f'{att}value.weight']
                rw = w[f'{att}receptance.weight']
                ow = w[f'{att}output.weight']
                if dd.stream:
                    kw = kw.to(device=dev, non_blocking=True)
                    vw = vw.to(device=dev, non_blocking=True)
                    rw = rw.to(device=dev, non_blocking=True)
                    ow = ow.to(device=dev, non_blocking=True)
                kmx = w[f'{att}key.weight_mx'] if wtype == torch.uint8 else x
                krx = w[f'{att}key.weight_rx'] if wtype == torch.uint8 else x
                kmy = w[f'{att}key.weight_my'] if wtype == torch.uint8 else x
                kry = w[f'{att}key.weight_ry'] if wtype == torch.uint8 else x
                vmx = w[f'{att}value.weight_mx'] if wtype == torch.uint8 else x
                vrx = w[f'{att}value.weight_rx'] if wtype == torch.uint8 else x
                vmy = w[f'{att}value.weight_my'] if wtype == torch.uint8 else x
                vry = w[f'{att}value.weight_ry'] if wtype == torch.uint8 else x
                rmx = w[f'{att}receptance.weight_mx'] if wtype == torch.uint8 else x
                rrx = w[f'{att}receptance.weight_rx'] if wtype == torch.uint8 else x
                rmy = w[f'{att}receptance.weight_my'] if wtype == torch.uint8 else x
                rry = w[f'{att}receptance.weight_ry'] if wtype == torch.uint8 else x
                omx = w[f'{att}output.weight_mx'] if wtype == torch.uint8 else x
                orx = w[f'{att}output.weight_rx'] if wtype == torch.uint8 else x
                omy = w[f'{att}output.weight_my'] if wtype == torch.uint8 else x
                ory = w[f'{att}output.weight_ry'] if wtype == torch.uint8 else x
                x, state[i*5+0], state[i*5+1], state[i*5+2], state[i*5+3] = ATT(
                    x, state[i*5+0], state[i*5+1], state[i*5+2], state[i*5+3],
                    w[f'{bbb}ln1.weight'], w[f'{bbb}ln1.bias'],
                    w[f'{att}time_mix_k'], w[f'{att}time_mix_v'], w[f'{att}time_mix_r'],
                    w[f'{att}time_decay'], w[f'{att}time_first'],
                    kw, vw, rw, ow,
                    kmx, krx, kmy, kry,
                    vmx, vrx, vmy, vry,
                    rmx, rrx, rmy, rry,
                    omx, orx, omy, ory,
                    )
                if dd.stream:
                    del kw, vw, rw, ow

                kw = w[f'{ffn}key.weight']
                vw = w[f'{ffn}value.weight']
                rw = w[f'{ffn}receptance.weight']
                if dd.stream:
                    kw = kw.to(device=dev, non_blocking=True)
                    vw = vw.to(device=dev, non_blocking=True)
                    rw = rw.to(device=dev, non_blocking=True)
                kmx = w[f'{ffn}key.weight_mx'] if wtype == torch.uint8 else x
                krx = w[f'{ffn}key.weight_rx'] if wtype == torch.uint8 else x
                kmy = w[f'{ffn}key.weight_my'] if wtype == torch.uint8 else x
                kry = w[f'{ffn}key.weight_ry'] if wtype == torch.uint8 else x
                vmx = w[f'{ffn}value.weight_mx'] if wtype == torch.uint8 else x
                vrx = w[f'{ffn}value.weight_rx'] if wtype == torch.uint8 else x
                vmy = w[f'{ffn}value.weight_my'] if wtype == torch.uint8 else x
                vry = w[f'{ffn}value.weight_ry'] if wtype == torch.uint8 else x
                rmx = w[f'{ffn}receptance.weight_mx'] if wtype == torch.uint8 else x
                rrx = w[f'{ffn}receptance.weight_rx'] if wtype == torch.uint8 else x
                rmy = w[f'{ffn}receptance.weight_my'] if wtype == torch.uint8 else x
                rry = w[f'{ffn}receptance.weight_ry'] if wtype == torch.uint8 else x                    
                x, state[i*5+4] = FFN(
                    x, state[i*5+4],
                    w[f'{bbb}ln2.weight'], w[f'{bbb}ln2.bias'],
                    w[f'{ffn}time_mix_k'], w[f'{ffn}time_mix_r'],
                    kw, vw, rw,
                    kmx, krx, kmy, kry,
                    vmx, vrx, vmy, vry,
                    rmx, rrx, rmy, rry,                    
                    )
                if dd.stream:                
                    del kw, vw, rw
                
                if self.RESCALE_LAYER > 0:
                    if (i+1) % self.RESCALE_LAYER == 0:
                        x = x / 2
            
            dd = self.strategy[args.n_layer]
            x = x[-1,:] if (seq_mode and (not full_output)) else x
            x = x.to(dtype=dd.atype, device=dd.device)
            
            x = F.layer_norm(x, (args.n_embd,), weight=w['ln_out.weight'], bias=w['ln_out.bias'])
            if w['head.weight'].dtype != torch.uint8:
                x = x @ w['head.weight']
            else:
                if seq_mode and full_output:
                    x = self.mm8_seq(x, w['head.weight'], w['head.weight_mx'], w['head.weight_rx'], w['head.weight_my'], w['head.weight_ry'])
                else:
                    x = self.mm8_one(x, w['head.weight'], w['head.weight_mx'], w['head.weight_rx'], w['head.weight_my'], w['head.weight_ry'])

            return x.float(), state
