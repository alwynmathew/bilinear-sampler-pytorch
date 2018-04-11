from __future__ import absolute_import, division, print_function
import torch
import torch.nn.functional as F
from torch.autograd import Variable

def bilinear_sampler_1d_h(input_images, x_offset, **kwargs):

	def _repeat(x, n_repeats):
		rep = x.unsqueeze(1).repeat(1, n_repeats)
		return rep.view(-1)

	def _interpolate(im, x, y):
		
		_edge_size = 0
		if _wrap_mode == 'border':
			_edge_size = 1
			im = F.pad(im,(0,1,1,0), 'constant', 0)
			x = x + _edge_size
			y = y + _edge_size
		elseif _wrap_mode == 'edge':
			_edge_size = 0
		else:
			return None

		x = torch.clamp(x, 0.0,  _width_f - 1)

		x0_f = torch.floor(x)
		y0_f = torch.floor(y)
		x1_f = x0_f + 1

		x0 = x0_f.type(torch.FloatTensor)
		y0 = y0_f.type(torch.FloatTensor)

		min_val = _width_f - 1
		scalar = torch.FloatTensor([min_val]).cuda()

		x1 = torch.min(x1_f, scalar)
		x1 = x1.type(torch.FloatTensor)
		dim2 = _width
		dim1 = _width * _height
		base = _repeat(torch.arange(_num_batch) * dim1, _height * _width)

		base_y0 = base + y0 * dim2
		idx_l = base_y0 + x0
		idx_r = base_y0 + x1
		idx_l = Variable(idx_l.type(torch.cuda.LongTensor))
		idx_r = Variable(idx_r.type(torch.cuda.LongTensor))

		im_flat = im.contiguous().view(-1) 

		pix_l = torch.gather(im_flat, 0, idx_l).unsqueeze(1)
		pix_r = torch.gather(im_flat, 0, idx_r).unsqueeze(1)

		weight_l = Variable((x1_f - x).unsqueeze(1))
		weight_r = Variable((x - x0_f).unsqueeze(1))

		return weight_l * pix_l + weight_r * pix_r

	def _transform(input_images, x_offset):

		a = torch.linspace(0.0, _width_f -1.0, _width).cuda()
		b = torch.linspace(0.0, _height_f -1.0, _height).cuda()

		x_t = a.repeat(_height)
		y_t = b.repeat(_width,1).t().contiguous().view(-1)

		x_t_flat = x_t.repeat(_num_batch, 1)
		y_t_flat = y_t.repeat(_num_batch, 1)

		x_t_flat = x_t_flat.view(-1)
		y_t_flat = y_t_flat.view(-1)

		x_t_flat = x_t_flat + x_offset.data.contiguous().view(-1) * _width_f

		input_transformed = _interpolate(input_images, x_t_flat, y_t_flat)

		output = input_transformed.view(_num_batch, _num_channels, _height, _width)

		return output

	_num_batch    = input_images.size(0)
	_num_channels = input_images.size(1)
	_height       = input_images.size(2)
	_width        = input_images.size(3)

	_height_f = float(_height)
	_width_f = float(_width)

	_wrap_mode = wrap_mode

	output = _transform(input_images, x_offset)

	return output
