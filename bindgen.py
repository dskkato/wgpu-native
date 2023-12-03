#!/usr/bin/env python3

import subprocess

types_to_rename = [
    ("WGPUAdapter", "WGPUAdapterImpl"),
    ("WGPUBindGroup", "WGPUBindGroupImpl"),
    ("WGPUBindGroupLayout", "WGPUBindGroupLayoutImpl"),
    ("WGPUBuffer", "WGPUBufferImpl"),
    ("WGPUCommandBuffer", "WGPUCommandBufferImpl"),
    ("WGPUCommandEncoder", "WGPUCommandEncoderImpl"),
    ("WGPUComputePassEncoder", "WGPUComputePassEncoderImpl"),
    ("WGPUComputePipeline", "WGPUComputePipelineImpl"),
    ("WGPUDevice", "WGPUDeviceImpl"),
    ("WGPUInstance", "WGPUInstanceImpl"),
    ("WGPUPipelineLayout", "WGPUPipelineLayoutImpl"),
    ("WGPUQuerySet", "WGPUQuerySetImpl"),
    ("WGPUQueue", "WGPUQueueImpl"),
    ("WGPURenderBundle", "WGPURenderBundleImpl"),
    ("WGPURenderBundleEncoder", "WGPURenderBundleEncoderImpl"),
    ("WGPURenderPassEncoder", "WGPURenderPassEncoderImpl"),
    ("WGPURenderPipeline", "WGPURenderPipelineImpl"),
    ("WGPUSampler", "WGPUSamplerImpl"),
    ("WGPUShaderModule", "WGPUShaderModuleImpl"),
    ("WGPUSurface", "WGPUSurfaceImpl"),
    ("WGPUTexture", "WGPUTextureImpl"),
    ("WGPUTextureView", "WGPUTextureViewImpl"),
]

blocklist_functions = ["--blocklist-function", "wgpuGetProcAddress"]
blocklist_types = []
raw_lines = []
for (old_name, new_name) in types_to_rename:
    line = f"pub type {old_name} = *const crate::{new_name};"
    blocklist_types.extend(["--blocklist-type", old_name])
    blocklist_types.extend(["--blocklist-type", f"{old_name}Impl"])
    raw_lines.extend(["--raw-line", line])

headers = [
    "ffi/wgpu.h",
    # "ffi/webgpu-headers/webgpu.h",
]

opts = ["--ignore-functions", "--no-prepend-enum-name"]
args = ["bindgen", *headers, *blocklist_functions, *blocklist_types, *raw_lines, *opts]
proc = subprocess.run(args, capture_output=True, check=True)

with open("src/bindings.rs", "w") as f:
    f.write(proc.stdout.decode("utf-8"))