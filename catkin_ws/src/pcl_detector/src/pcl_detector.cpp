#include <ros/ros.h>
// PCL specific includes
#include <sensor_msgs/PointCloud2.h>
#include <geometry_msgs/PointStamped.h>
#include <visualization_msgs/Marker.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/point_cloud.h>
#include <pcl/point_types.h>
#include <pcl/filters/filter.h>
#include "pcl_ros/point_cloud.h"
#include <pcl/common/common.h>
#include <pcl/filters/voxel_grid.h>

#include <vibration_msgs/VibrationArray.h>

ros::Publisher pub_vb_cmd;
typedef pcl::PointCloud<pcl::PointXYZ> PointCloudXYZ;

void  cloud_cb (const sensor_msgs::PointCloud2ConstPtr& input)
{

	PointCloudXYZ::Ptr cloud(new PointCloudXYZ);
	pcl::fromROSMsg (*input, *cloud); //convert from PointCloud2 to pcl point type
  //Exmaple : pcl PointCloudXYZRGB information
  std::vector<int> indices;
  pcl::removeNaNFromPointCloud(*cloud, *cloud, indices);
  pcl::VoxelGrid<pcl::PointXYZ> sor;
  sor.setInputCloud (cloud);
  sor.setLeafSize (0.005f, 0.005f, 0.005f);
  sor.filter (*cloud);
  printf("-------------------------Cloud information-----------------------------\n");
  printf("cloud size: %d\n",cloud->points.size());
  int cloud_size=cloud->points.size();
  //----------------------------------------------------------------------
  //process cloud here
  //find out where are the obstacles, left, front or right
  //---------------------------------------------------------------------
  vibration_msgs::VibrationArray vbArray;
  for(int i=0; i<3; i++){
    vbArray.frequencies.push_back(3);
    vbArray.intensities.push_back(0);
  }
  //---------------------------------------------------------------------
  //According to the result of your algorithm, decide which motor should vibrate
  // 0 for left, 1 for front, 2 for right 
  //vbArray.intensities[0] = XXX;
  //vbArray.intensities[1] = XXX;
  //vbArray.intensities[2] = XXX;
  //----------------------------------------------------------------------
  printf("left: %d, front: %d, right: %d \n", vbArray.intensities[0], vbArray.intensities[1], vbArray.intensities[2]);
  pub_vb_cmd.publish(vbArray);
}   
int   main (int argc, char** argv)
{
     // Initialize ROS
     ros::init (argc, argv, "my_pcl_tutorial");
     ros::NodeHandle nh;   
     // Create a ROS subscriber for the input point cloud
     ros::Subscriber model_subscriber = nh.subscribe<sensor_msgs::PointCloud2> ("/camera/depth/points", 1, cloud_cb);
     pub_vb_cmd = nh.advertise<vibration_msgs::VibrationArray> ("vibrate_cmd", 1);
     // Spin
     ros::spin ();
  }
