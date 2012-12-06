#include <stdio.h>
#include <stdlib.h>
#include "header.h"
#include "util.h"

#define BLOCK_DIM	16

__global__ void gpu_diffterm_lv3_kernel(
	global_const_t *g,			// i: Global struct containing application parameters
	double *q,					// i:
	double *difflux,			// o:
	double *flux				// o: set zeroes for hypterm
){
	int si, sj, sk, idx, idx_g;
	double mechwork;

	si = blockIdx.x*blockDim.x + threadIdx.x;
	sj = blockIdx.y*blockDim.y + threadIdx.y;
	sk = blockIdx.z;

	idx = sk*g->plane_offset_padded + sj*g->pitch[0] + si;
	idx_g	= (sk+g->ng)*g->plane_offset_g_padded + (sj+g->ng)*g->pitch_g[0] + si+g->ng;
	if(si < g->dim[0] && sj < g->dim[1] && sk < g->dim[2]){

		mechwork = 	difflux[idx + iene*g->comp_offset_padded] +
					difflux[idx + imz*g->comp_offset_padded]*q[idx_g + qw*g->comp_offset_g_padded];
		difflux[idx + iene*g->comp_offset_padded] =
					g->alam*(g->temp[TXX][idx]+g->temp[TYY][idx]+g->temp[TZZ][idx]) + mechwork;
	}
}

void gpu_diffterm2(
	global_const_t h_const, 	// i: Global struct containing application parameters
	global_const_t *d_const,	// i: Device pointer to global struct containing application paramters
	double *d_q,				// i:
	double *d_difflux,			// o:
	double *d_flux				// o: just set zeroes for hypterm
){
	kernel_const_t h_kc;
	dim3 grid_dim(CEIL(h_const.dim_g[0], BLOCK_DIM), CEIL(h_const.dim_g[1], BLOCK_DIM), h_const.dim_g[2]);
	dim3 block_dim(BLOCK_DIM, BLOCK_DIM);

	gpu_diffterm_lv1_lv2(h_const, d_const, d_q, d_difflux, d_flux);
	gpu_diffterm_lv3_kernel<<<grid_dim, block_dim>>>(d_const, d_q, d_difflux, d_flux);
}
