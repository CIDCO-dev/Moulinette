#include <iostream>
#include <vector>
#include <numeric>
#include <string.h>
#include <sstream>
#include "../math/CoordinateTransform.hpp"
#include "../Position.hpp"

int main(int argc, const char* argv[]) {
    
	// std::cerr << "cat FILE | ./wgs2ecef"<<std::endl;
	// compile in examples directory of mbes with command
	// g++ -I /usr/include/eigen3 wgs2ecef.cpp -o wgs2ecef
	
	double lon;
	double lat;
	double ellipsoidalHeight;
	std::string line;
	
	while ( std::getline( std::cin, line ) ) {
		
	    std::istringstream stream( line );

	    if ( 3 == sscanf(line.c_str(), "%lf %lf %lf", &lon, &lat, &ellipsoidalHeight)) { 
	    	try{
				Eigen::Vector3d positionECEF(0,0,0);
				Position position(0,lon, lat, ellipsoidalHeight);
				CoordinateTransform::getPositionECEF(positionECEF, position);
				std::cout<<positionECEF(0)<<" "<<positionECEF(1)<<" "<<positionECEF(2)<<std::endl;	
				
			}
			catch(std::exception & e){
				std::cerr <<  e.what() << std::endl;
			}
		}
		else{
			std::cerr<<"error " << std::endl;
		}
	}
	return 0;
}
