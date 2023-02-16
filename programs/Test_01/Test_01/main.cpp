//#include "sender.h"
#include "sender2.h"
#include "camera.h"

#include <iostream>
#include <cstdlib>
#include <thread>

int main()
{

	bool send = 1;
	bool receive = 0;

	if (send && receive) {

		//std::thread t1(sendCamera, 0);		
		std::thread t2(readCamera, 0, 1);

		//t1.join();
		t2.join();
					
	}

	else if (send) {
		
		std::thread t0(sendCamera, 0);		
		std::thread t1(sendCamera, 1);
		std::thread t2(sendCamera, 2);
		std::thread t6(sendCamera, 6);
		std::thread t7(sendCamera, 7);				

		t0.join();		
		t1.join();
		t2.join();
		t6.join();
		t7.join();		
		
	}
	else {

		//std::thread t1(readCamera, 0, 4);
		int nCameras = 4;

		// Create the display threads
		std::thread t1(readCamera, 0, nCameras);
		std::thread t2(readCamera, 1, nCameras);
		std::thread t3(readCamera, 2, nCameras);
		std::thread t4(readCamera, 3, nCameras);

		// Wait for the threads to finish
		t1.join();
		t2.join();
		t3.join();
		t4.join();

	}

	// Finished
	return 0;
}