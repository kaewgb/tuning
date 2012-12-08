
def ceiling(x, y):
	return (x+y-1)/y*y;

block_dim_choices 	= [4, 8, 16, 32, 64, 128, 256];
thread_z_choices 	= [4, 8, 16, 32, 64];
maxrreg_choices		= [16, 20, 24, 28, 32];
pad_choices			= [32, 128, 256];
smem_choices		= [16, 48];
bypass_l1_choices	= [0, 1];

ng = 4;
global_pad = 128;

for block_dim_x in block_dim_choices:
	for block_dim_y in block_dim_choices:
		for thread_z in thread_z_choices:
			for maxrreg in maxrreg_choices:
				for shared_pad in pad_choices:
					for smem in smem_choices:
						for bypass_l1 in bypass_l1_choices:
							if smem == 16 and ceiling((block_dim_x+ng+ng)*8, shared_pad)*(block_dim_y+ng+ng) > 16*1024:
								continue;
							elif smem == 48 and ceiling((block_dim_x+ng+ng)*8, shared_pad)*(block_dim_y+ng+ng) > 48*1024:
								continue;
							print block_dim_x, block_dim_y, thread_z, maxrreg, global_pad, shared_pad, smem, bypass_l1
