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
	// Variables	
	int currentFrame = 0;
	int nFrames = 69;

	std::vector<std::vector<unsigned char>> frames = std::vector<std::vector<unsigned char>>(nFrames);

	// Lets load the file from disk
	std::vector<unsigned char> png_data;

	int n_zero = 4;

	// Not required, but "correct" (see the SDK documentation).
	if (!NDIlib_initialize()) {
		// Cannot run NDI. Most likely because the CPU is not sufficient (see SDK documentation).
		// you can check this directly with a call to NDIlib_is_supported_CPU()
		printf("Cannot run NDI.");
		return 0;
	}		


	for (int i = 0; i < nFrames; i++) {
		
		std::string old_str = std::to_string(i+1);
		auto new_str = std::string(n_zero - std::min(n_zero, static_cast<int>(old_str.length())), '0') + old_str;		
	
		// create a string that contains the path to the image	
		std::string filename = "C:\\Users\\Sebastian Cavada\\Documents\\SCSV\\Thesis\\_images\\Synthetic\\Animation_medium_distortion\\Cam" + std::to_string(cameraIdx) + "\\DigitalTwinSequence." + new_str +  ".png";

		loadFile(frames[i], filename);
		if (frames[i].empty())
			return 0;				
		
	}		

	// Create an NDI source that is called "My PNG" and is clocked to the video.
	NDIlib_send_create_t NDI_send_create_desc;
	string a = "cam-" + std::to_string(cameraIdx);
	NDI_send_create_desc.p_ndi_name = a.c_str();

	// We create the NDI sender
	NDIlib_send_instance_t pNDI_send = NDIlib_send_create(&NDI_send_create_desc);
	if (!pNDI_send)
		return 0;	

	// Decode the PNG file
	std::vector<unsigned char> image_data;
	unsigned long xres = 0, yres = 0;

	// Decode the PNG file
	std::vector<std::vector<unsigned char>> images = std::vector<std::vector<unsigned char>>(nFrames);	

	for (int i = 0; i < nFrames; i++) {
		if (decodePNG(images[i], xres, yres, &frames[i][0], frames[i].size(), true))
			return 0;
	}

	//delete the frames;
	frames.clear();		

	// We are going to create a frame
	NDIlib_video_frame_v2_t NDI_video_frame;
	NDI_video_frame.xres = xres;
	NDI_video_frame.yres = yres;
	NDI_video_frame.FourCC = NDIlib_FourCC_type_RGBA;
	NDI_video_frame.line_stride_in_bytes = xres * 4;
	NDI_video_frame.frame_rate_N = 30000;
	NDI_video_frame.frame_rate_D = 1001;
	NDI_video_frame.picture_aspect_ratio = 16.0f / 9.0f;
	NDI_video_frame.frame_format_type = NDIlib_frame_format_type_progressive;
	NDI_video_frame.timecode = 0;

	// We now submit the frame. Note that this call will be clocked so that we end up submitting at exactly 29.97fps.
	while (true) {		
		
		NDI_video_frame.p_data = &images[currentFrame][0];

		NDIlib_send_send_video_v2(pNDI_send, &NDI_video_frame);

		if (currentFrame == nFrames-1)
		{
			currentFrame = 0;
		}
		else
		{
			currentFrame++;
		}

		// Sleep for 16ms
		std::this_thread::sleep_for(std::chrono::milliseconds(1000));		
		
	}

	// Destroy the NDI sender
	NDIlib_send_destroy(pNDI_send);

	// Not required, but nice
	NDIlib_destroy();

	// Success
	return 0;
}