#include <ros.h>
#include <ros/time.h>
#include <sensor_msgs/Range.h>

ros::NodeHandle n;

sensor_msgs::Range msg_1;
sensor_msgs::Range msg_2;
sensor_msgs::Range msg_3;
sensor_msgs::Range msg_4;
sensor_msgs::Range msg_5;
sensor_msgs::Range msg_6;

ros::Publisher pub_sensor_1("/distance_sensor/1", &msg_1);
ros::Publisher pub_sensor_2("/distance_sensor/2", &msg_2);
ros::Publisher pub_sensor_3("/distance_sensor/3", &msg_3);
ros::Publisher pub_sensor_4("/distance_sensor/4", &msg_4);
ros::Publisher pub_sensor_5("/distance_sensor/5", &msg_5);
ros::Publisher pub_sensor_6("/distance_sensor/6", &msg_6);

const int echo_1 = 12;
const int trig_1 = 13;
const int echo_2 = 10;
const int trig_2 = 11;
const int echo_3 = 8;
const int trig_3 = 9;
const int echo_4 = 6;
const int trig_4 = 7;
const int echo_5 = 2;
const int trig_5 = 3;
const int echo_6 = 4;
const int trig_6 = 5;

void setup()
{
	n.initNode();
	n.advertise(pub_sensor_1);
	n.advertise(pub_sensor_2);
	n.advertise(pub_sensor_3);
	n.advertise(pub_sensor_4);
	n.advertise(pub_sensor_5);
	n.advertise(pub_sensor_6);

	msg_1.radiation_type = sensor_msgs::Range::ULTRASOUND;
	msg_1.header.frame_id = "/sensor_1";
	msg_1.field_of_view = 0.1; //dummy, irrelevant in our case
	msg_1.min_range = 0.02;
	msg_1.max_range = 4.0;

	msg_2.radiation_type = sensor_msgs::Range::ULTRASOUND;
	msg_2.header.frame_id = "/sensor_2";
	msg_2.field_of_view = 0.1; //dummy, irrelevant in our case
	msg_2.min_range = 0.02;
	msg_2.max_range = 4.0;

	msg_3.radiation_type = sensor_msgs::Range::ULTRASOUND;
	msg_3.header.frame_id = "/sensor_3";
	msg_3.field_of_view = 0.1; //dummy, irrelevant in our case
	msg_3.min_range = 0.02;
	msg_3.max_range = 4.0;

	msg_4.radiation_type = sensor_msgs::Range::ULTRASOUND;
	msg_4.header.frame_id = "/sensor_4";
	msg_4.field_of_view = 0.1; //dummy, irrelevant in our case
	msg_4.min_range = 0.02;
	msg_4.max_range = 4.0;

	msg_5.radiation_type = sensor_msgs::Range::ULTRASOUND;
	msg_5.header.frame_id = "/sensor_5";
	msg_5.field_of_view = 0.1; //dummy, irrelevant in our case
	msg_5.min_range = 0.02;
	msg_5.max_range = 4.0;

	msg_6.radiation_type = sensor_msgs::Range::ULTRASOUND;
	msg_6.header.frame_id = "/sensor_6";
	msg_6.field_of_view = 0.1; //dummy, irrelevant in our case
	msg_6.min_range = 0.02;
	msg_6.max_range = 4.0;

	pinMode(echo_1, INPUT);
	pinMode(trig_1, OUTPUT);
	pinMode(echo_2, INPUT);
	pinMode(trig_2, OUTPUT);
	pinMode(echo_3, INPUT);
	pinMode(trig_3, OUTPUT);
	pinMode(echo_4, INPUT);
	pinMode(trig_4, OUTPUT);
	pinMode(echo_5, INPUT);
	pinMode(trig_5, OUTPUT);
	pinMode(echo_6, INPUT);
	pinMode(trig_6, OUTPUT);
}

void loop()
{
	msg_1.range = dist_calc(trig_1, echo_1);
	msg_1.header.stamp = n.now();
	pub_sensor_1.publish(&msg_1);

	msg_2.range = dist_calc(trig_2, echo_2);
	msg_2.header.stamp = n.now();
	pub_sensor_2.publish(&msg_2);

	msg_3.range = dist_calc(trig_3, echo_3);
	msg_3.header.stamp = n.now();
	pub_sensor_3.publish(&msg_3);

	msg_4.range = dist_calc(trig_4, echo_4);
	msg_4.header.stamp = n.now();
	pub_sensor_4.publish(&msg_4);

	msg_5.range = dist_calc(trig_5, echo_5);
	msg_5.header.stamp = n.now();
	pub_sensor_5.publish(&msg_5);

	msg_6.range = dist_calc(trig_6, echo_6);
	msg_6.header.stamp = n.now();
	pub_sensor_6.publish(&msg_6);

	n.spinOnce();
	delay(50);
}

float dist_calc(int trig, int echo)
{
	digitalWrite(trig,LOW);
	delayMicroseconds(2);
	digitalWrite(trig,HIGH);
	delayMicroseconds(10);
	digitalWrite(trig,LOW);
	float time = pulseIn(echo,HIGH);
	float dist = (0.00034*time)/2.0;
	dist > 4.0 ? dist = 4.0 : dist = dist;
	return dist;
}
