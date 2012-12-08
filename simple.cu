#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include "header.h"
#include "util.cuh"
#include "util.h"

#define BLOCK_SMALL		8
#define	BLOCK_LARGE		16
#define	THREAD_Z		8

__global__ void gpu_simple_stencil_kernel(
	global_const_t *g,	// i:
	double *q,			// i:
	double *flux		// o:
){
	bool compute=false;
	int z, zidx, idx,out,si,sj,sk,tidx,tidy;
	double unp1, unp2, unp3, unp4, unm1, unm2, unm3, unm4;
	double flux_irho;

	__shared__ double      s_qu[BLOCK_LARGE+NG+NG][BLOCK_LARGE+NG+NG];

	// Load to shared mem
	for(z=0;z<THREAD_Z;z++){

		si = blockIdx.x*blockDim.x+threadIdx.x;
		sj = blockIdx.y*blockDim.y+threadIdx.y;
		sk = (blockIdx.z*blockDim.z+threadIdx.z)*THREAD_Z + z;

		out = sk*g->plane_offset_padded + sj*g->pitch[0] + si;
		compute = (si < g->dim[0] && sj < g->dim[1] && sk < g->dim[2]);


		__syncthreads();	//for the next z round
		for(sj=blockIdx.y*blockDim.y+threadIdx.y, tidy=threadIdx.y; tidy < BLOCK_LARGE+NG+NG; sj+=blockDim.y, tidy+=blockDim.y){
			for(si=blockIdx.x*blockDim.x+threadIdx.x, tidx=threadIdx.x; tidx < BLOCK_LARGE+NG+NG; si+=blockDim.x, tidx+=blockDim.x){
				if( si < g->dim_g[0] && sj < g->dim_g[1] && sk < g->dim_g[2]){

					idx = (sk+g->ng)*g->plane_offset_g_padded + sj*g->pitch_g[0] + si;
					s_qu[tidy][tidx] = q[idx + qu*g->comp_offset_g_padded];

				}
			}
		}
		__syncthreads();

		if(compute){

	#define	s_qu(i)			s_qu[threadIdx.y+g->ng][threadIdx.x+g->ng+(i)]

			flux_irho = - ( g->ALP*(s_qu(1)-s_qu(-1))
						  + g->BET*(s_qu(2)-s_qu(-2))
						  + g->GAM*(s_qu(3)-s_qu(-3))
						  + g->DEL*(s_qu(4)-s_qu(-4)))*g->dxinv[0];

			flux_irho -=  ( g->ALP*(s_qu(1)-s_qu(-1))
						  + g->BET*(s_qu(2)-s_qu(-2))
						  + g->GAM*(s_qu(3)-s_qu(-3))
						  + g->DEL*(s_qu(4)-s_qu(-4)))*g->dxinv[1];

	#undef	s_qu

		}

		/** Z dimension **/
		si = blockIdx.x*blockDim.x+threadIdx.x;
		sj = blockIdx.y*blockDim.y+threadIdx.y;
		if(compute){
			idx = (sk+g->ng)*g->plane_offset_g_padded + (sj+g->ng)*g->pitch_g[0] + si+g->ng;

			unp1 = q[qu*g->comp_offset_g_padded + idx + 1*g->plane_offset_g_padded];
			unp2 = q[qu*g->comp_offset_g_padded + idx + 2*g->plane_offset_g_padded];
			unp3 = q[qu*g->comp_offset_g_padded + idx + 3*g->plane_offset_g_padded];
			unp4 = q[qu*g->comp_offset_g_padded + idx + 4*g->plane_offset_g_padded];
			unm1 = q[qu*g->comp_offset_g_padded + idx - 1*g->plane_offset_g_padded];
			unm2 = q[qu*g->comp_offset_g_padded + idx - 2*g->plane_offset_g_padded];
			unm3 = q[qu*g->comp_offset_g_padded + idx - 3*g->plane_offset_g_padded];
			unm4 = q[qu*g->comp_offset_g_padded + idx - 4*g->plane_offset_g_padded];


			flux_irho -=  ( g->ALP*(unp1-unm1)
						  + g->BET*(unp2-unm2)
						  + g->GAM*(unp3-unm3)
						  + g->DEL*(unp4-unm4))*g->dxinv[2];

			// Update global memory
			flux[out + irho*g->comp_offset_padded] = flux_irho;

		}
	}
}

__global__ void usleep(){
	clock_t start = clock();
	clock_t now = clock();
	clock_t cycles;

	do{
		cycles = (now > start)? (now-start):(now+(0xffffffff - start));
		now = clock();

	}while(cycles < CLOCKS_PER_SEC);
}

void gpu_simple_stencil(
	global_const_t h_const, 	// i: Global struct containing application parameters
	global_const_t *d_const,	// i: Device pointer to global struct containing application paramters
	double *d_q,				// i:
	double *d_flux				// o:
){
	// Set preferred cache configuration (48KB smem | 16KB smem)
	// cudaFuncCachePreferShared | cudaFuncCachePreferL1
	cudaDeviceSetCacheConfig(cudaFuncCachePreferL1);

	dim3 block_dim(BLOCK_LARGE, BLOCK_LARGE, 1);
	dim3 grid_dim(CEIL(h_const.dim[0], BLOCK_LARGE), CEIL(h_const.dim[1], BLOCK_LARGE), CEIL(h_const.dim[2], THREAD_Z));


	struct timeval s, e;
	gettimeofday(&s, NULL);

	cudaEvent_t start, stop;
	cudaEventCreate(&start);
	cudaEventCreate(&stop);

	cudaEventRecord(start, 0);
	gpu_simple_stencil_kernel<<<grid_dim, block_dim>>>(d_const, d_q, d_flux);
//	usleep<<<grid_dim, block_dim>>>();
	cudaEventRecord(stop, 0);
	cudaEventSynchronize(stop);

	cudaThreadSynchronize();
	gettimeofday(&e, NULL);

	float elapsedTime;
	cudaEventElapsedTime(&elapsedTime, start, stop);
	printf("%lf vs %lf\n", elapsedTime, (double)(e.tv_sec-s.tv_sec) + 1.0E-6*(e.tv_usec-s.tv_usec));

	cudaEventDestroy(start);
	cudaEventDestroy(stop);
}
