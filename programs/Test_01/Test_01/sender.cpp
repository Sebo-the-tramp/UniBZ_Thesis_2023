/*
#include <stdlib.h>
#include <chrono>
#include <thread>
#include <Processing.NDI.Lib.h>

#include <iostream>
#include <string>

#ifdef _WIN32
#ifdef _WIN64
#pragma comment(lib, "Processing.NDI.Lib.x64.lib")
#else // _WIN64
#pragma comment(lib, "Processing.NDI.Lib.x86.lib")
#endif // _WIN64
#endif

// PNG loader in a single file !
// From http://lodev.org/lodepng/ 
#include "picopng.hpp"

using namespace std;

int sendCamera(int cameraIdx)
{
	// Not required, but "correct" (see the SDK documentation).
	if (!NDIlib_initialize()) {
		// Cannot run NDI. Most likely because the CPU is not sufficient (see SDK documentation).
		// you can check this directly with a call to NDIlib_is_supported_CPU()
		printf("Cannot run NDI.");
		return 0;
	}

	// Lets load the file from disk
	std::vector<unsigned char> png_data;
	
	// create a string that contains the path to the image	
	std::string filename = "C:\\Users\\Sebastian Cavada\\Documents\\SCSV\\Thesis\\_data\\NEW\\Cam" + std::to_string(cameraIdx) + "\\DigitalTwinSequence.0001.png";

	loadFile(png_data, filename);
	if (png_data.empty())
		return 0;

	// Decode the PNG file
	std::vector<unsigned char> image_data;
	unsigned long xres = 0, yres = 0;
	if (decodePNG(image_data, xres, yres, &png_data[0], png_data.size(), true))
		return 0;

	// Create an NDI source that is called "My PNG" and is clocked to the video.
	NDIlib_send_create_t NDI_send_create_desc;
	string a = "cam-" + std::to_string(cameraIdx);
	NDI_send_create_desc.p_ndi_name = a.c_str();	

	// We create the NDI sender
	NDIlib_send_instance_t pNDI_send = NDIlib_send_create(&NDI_send_create_desc);
	if (!pNDI_send)
		return 0;	

	// We are going to create a frame
	NDIlib_video_frame_v2_t NDI_video_frame;
	NDI_video_frame.xres = xres;
	NDI_video_frame.yres = yres;
	NDI_video_frame.FourCC = NDIlib_FourCC_type_RGBA;
	NDI_video_frame.p_data = &image_data[0];
	NDI_video_frame.line_stride_in_bytes = xres * 4;
	NDI_video_frame.frame_rate_N = 30000;
	NDI_video_frame.frame_rate_D = 1001;
	NDI_video_frame.picture_aspect_ratio = 16.0f / 9.0f;
	NDI_video_frame.frame_format_type = NDIlib_frame_format_type_progressive;
	NDI_video_frame.timecode = 0;

	// We now submit the frame. Note that this call will be clocked so that we end up submitting at exactly 29.97fps.
	while (true) {

		NDIlib_send_send_video_v2(pNDI_send, &NDI_video_frame);			
		
		// Sleep for 16ms
		std::this_thread::sleep_for(std::chrono::milliseconds(16));
	}		

	// Destroy the NDI sender
	NDIlib_send_destroy(pNDI_send);

	// Not required, but nice
	NDIlib_destroy();

	// Success
	return 0;
}

*/