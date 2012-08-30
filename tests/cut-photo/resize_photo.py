#coding:utf8

from libjade import *
from PIL import Image

def load_image(fp_src):
	return Image.open(fp_src)

def save_image(img, fp_dst):
	img.save(fp_dst)
	
def slice_image(img, left, top, right, bottom):
	box = (int(left), int(top), int(right), int(bottom))
	region = img.crop(box)
	return region
	
def cut_image(img, x, y, w, h):
	return slice_image(img, x, y, x+w, y+h)
	
def resize_image(img, w, h):
	# new_img=img.resize((w, h), Image.BILINEAR)
	new_img=img.resize((w, h), Image.ANTIALIAS)
	return new_img

def cut_photo(fp_src, fp_dst, x, y, w, h, width, height, stretch):
	src=0
	cut=0
	new=0
	try:
		src=load_image(fp_src)
		if not src:
			debug('cut_photo: unable to load image from %s' % fp_src)
			return -1
		
		zoom_mode=False
		if x==0 and y==0 and w==0 and h==0: zoom_mode=True
		
		src_width, src_height=src.size
		
		if src_width==0 or src_height==0:
			debug('cut_photo: maybe not a picture')
			return -2
			
		if not zoom_mode:
			if not (x>=0 and y>=0 and w>0 and h>0 and width>0 and height>0):
				debug('cut_photo: bad parameters')
				return 1
				
			if not (x<=src_width and y<=src_height):
				debug('cut_photo: x and y should be inside the picture area')
				return 1
				
			if not (x+w<=src_width and y+h<=src_height):
				debug('cut_photo: bad parameters')
				return 2
				
			cut=cut_image(src, x, y, w, h)
			new=resize_image(cut, width, height)
			save_image(new, fp_dst)
			
			del src
			del cut
			del new
		else:
			if not (width>0 and height>0):
				debug('cut_photo: bad parameters')
				return 1
				
			if src_width<width and src_height<height and False==stretch:
				debug('cut_photo: no new picture is generated, keep the old picture')
				return 4
				
			src_w_div_h=1.0 * src_width / src_height
			dst_w_div_h=1.0 * width / height
			
			# print 'src_w_div_h=', src_w_div_h
			# print 'dst_w_div_h=', dst_w_div_h
			
			if src_w_div_h < dst_w_div_h:
				# width=int ( float(height) / src_height * src_width )
				width=int ( height * src_w_div_h )
			else:
				# height=int ( float(width) / src_width * src_height )
				height=int ( width / src_w_div_h )
			
			debug('in cut_photo, src_width=%f src_height=%f' % (src_width, src_height))
			new=resize_image(src, width, height)
			save_image(new, fp_dst)
			
			del src
			del new
			
		return 0
	except Exception, e:
		msg='''cut_photo: opencv inner error when cutting a image
		Exception:%s
		src fp:%s
		''' % (e, fp_src)
		error(msg)
		return 3
	
def auto_resize_photos_in_dir(max_width, max_height, src_dir_path, dst_dir_path=None):
	if not dst_dir_path: dst_dir_path='%s_%d_%d' % (src_dir_path, max_width, max_height)
	if not isdir(dst_dir_path): md(dst_dir_path)
	fns=listdir(src_dir_path)
	for fn in fns:
		fp_src=join(src_dir_path, fn)
		ext=splitext(fn)[-1][1:].lower()
		fp_dst=join(dst_dir_path, fn)
		if not ext in ['jpg', 'jpeg', 'gif', 'png', 'bmp', 'tif', 'tiff']: continue
		src=load_image(fp_src)
		
		if not src:
			debug('unable to load image from %s' % fp_src)
			continue
			
		src_width, src_height=src.size
		if src_width<=max_width and src_height<=max_height and fp_src!=fp_dst:
			save_image(src, fp_dst)
			debug('save_image from %s to %s' % (fp_src, fp_dst))
			del src
			continue
			
		src_w_div_h=1.0 * src_width / src_height
		dst_w_div_h=1.0 * max_width / max_height
		
		if src_w_div_h < dst_w_div_h:
			dst_width=int ( max_height * src_w_div_h )
			dst_height=max_height
		else:
			dst_width=max_width
			dst_height=int ( max_width / src_w_div_h )
		
		debug('src_width=%f src_height=%f, dst_width=%f dst_height=%f' % (src_width, src_height, dst_width, dst_height))
		
		dst=resize_image(src, dst_width, dst_height)
		
		save_image(dst, fp_dst)
		debug('save_image from %s to %s' % (fp_src, fp_dst))
		
		del src
		del dst
	
def test_cut():
	fp_src='a.jpg'
	fp_dst='cut.jpg'
	x=100
	y=100
	w=100
	h=100
	width=500
	height=500
	stretch=0
	cut_photo(fp_src, fp_dst, x, y, w, h, width, height, stretch)
	
def test_zoom():
	fp_src='a.jpg'
	fp_dst='zoom.jpg'
	x=0
	y=0
	w=0
	h=0
	width=200
	height=500
	stretch=0
	cut_photo(fp_src, fp_dst, x, y, w, h, width, height, stretch)
	

if __name__=='__main__':
	if argc!=2: 
		print 'usage: resize_photo.py <src_dir>'
		exit()
	src_dir=argv[1]
	auto_resize_photos_in_dir(800, 600, src_dir)
	
	