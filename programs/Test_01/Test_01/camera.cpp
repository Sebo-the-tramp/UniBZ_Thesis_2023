#include <cstdio>
#include <chrono>
#include <Processing.NDI.Lib.h>

#include <opencv2/core.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/imgcodecs.hpp>

#include <stdio.h>
#include <opencv2/imgproc.hpp>

#ifdef _WIN32
#ifdef _WIN64
#pragma comment(lib, "Processing.NDI.Lib.x64.lib")
#else // _WIN64
#pragma comment(lib, "Processing.NDI.Lib.x86.lib")
#endif // _WIN64
#endif // _WIN32

using namespace cv;
using namespace std;

int readCamera(int index, int nCameras)
{
	// Not required, but "correct" (see the SDK documentation).
	if (!NDIlib_initialize())
		return 0;
	
	// Create a finder
	NDIlib_find_instance_t pNDI_find = NDIlib_find_create_v2();
	if (!pNDI_find)
		return 0;
	
	// Wait until there is one source
	uint32_t no_sources = 0;
	const NDIlib_source_t* p_sources = NULL;
	while (!no_sources) {
		// Wait until the sources on the network have changed
		printf("Looking for sources ...\n");
		NDIlib_find_wait_for_sources(pNDI_find, 1000/* One second */);
		p_sources = NDIlib_find_get_current_sources(pNDI_find, &no_sources);
	}
		
	// Display all the sources.
	printf("Network sources (%u found).\n", no_sources);
	for (uint32_t i = 0; i < no_sources; i++)
		printf("%u. %s  %s\n", i + 1, p_sources[i].p_ndi_name, p_sources[i].p_url_address);		

	// Create an NDI receiver
	NDIlib_recv_create_v3_t recv_create_desc;

	//qui ho perso due giorni di lavoro
	recv_create_desc.color_format = NDIlib_recv_color_format_BGRX_BGRA;
	NDIlib_recv_instance_t pNDI_recv = NDIlib_recv_create_v3(&recv_create_desc);
	if (!pNDI_recv) {
		// Failed to create the NDI receiver
		return 1;
	}

	// Connect the NDI receiver to the custom camera's NDI source	
	NDIlib_recv_connect(pNDI_recv, p_sources + index);			

	Mat frame(720, 1280, CV_8UC4);
	Mat dst(720, 1280, CV_8UC3);

	String windowName = "NDI Camera " + to_string(index);

	// Run for one minute
	using namespace std::chrono;
	for (const auto start = high_resolution_clock::now(); high_resolution_clock::now() - start < minutes(5);) {
		// The descriptors
		NDIlib_video_frame_v2_t video_frame;

		switch (NDIlib_recv_capture_v2(pNDI_recv, &video_frame, nullptr, nullptr, 500)) {
			// No data
		case NDIlib_frame_type_none:
			printf("No data received.\n");
			break;

			// Video data
		case NDIlib_frame_type_video:
		{			

			printf("Data received\n");
			frame.data = video_frame.p_data;
				
			cvtColor(frame, dst, COLOR_BGRA2BGR);

			// check if we succeeded
			if (dst.empty()) {
				break;
			}
			
			// show live and wait for a key with timeout long enough to show images			
			namedWindow(windowName, cv::WINDOW_NORMAL);			

			// given the number of windows and the index position the window in the respective quadrant of the screen
			int x = (index % 2) * 1280 / max(1,(nCameras / 2));
			int y = (index / 2) * 720 / max(1, (nCameras / 2));
			moveWindow(windowName, 0, 0);
						
			// given the number of windows and the index resize the window in the respective quadrant of the screen
			int width = 1280 / max(1, (nCameras / 2));
			int height = 720 / 2;		
			resizeWindow(windowName, 1280, 720);		
			
			imshow(windowName, dst);
			if (waitKey(5) >= 0)				
				break;													
			
			//destroyWindow(windowName);//close the window and release allocate memory//
			NDIlib_recv_free_video_v2(pNDI_recv, &video_frame);
			
			break;
		}
		}
	}

	// Destroy the receiver
	NDIlib_recv_destroy(pNDI_recv);

	// Not required, but nice
	NDIlib_destroy();

	// Finished
	return 0;
}