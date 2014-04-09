"""
Publishes the Referee Box's messages as a ROS topic named "refbox" with type "referee"

"""

from referee_pb2 import SSL_Referee
import rospy

# Substitute "ekbots" here with your ROS package name
from ekbots.msg import referee, team_info

from socket import socket, inet_aton, IPPROTO_IP, IP_ADD_MEMBERSHIP
from socket import AF_INET, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, INADDR_ANY
import struct

pub = rospy.Publisher('refbox', referee)
rospy.init_node('refbox')
r = rospy.Rate(10) 


# Setup socket
MCAST_GRP   = "224.5.23.1"
MCAST_PORT  = 10003
BUFFER_SIZE = 1024

sock = socket(AF_INET, SOCK_DGRAM)
sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
mreq = struct.pack('=4sl', inet_aton(MCAST_GRP), INADDR_ANY) # pack MCAST_GRP correctly
sock.setsockopt(IPPROTO_IP, IP_ADD_MEMBERSHIP, mreq)         # Request MCAST_GRP

sock.bind((MCAST_GRP, MCAST_PORT))                           # Bind to all interfaces


while not rospy.is_shutdown():
	# Receive the protobuff from the network
	data, addr = sock.recvfrom(BUFFER_SIZE)  # NOTE: This call is blocking

	proto = SSL_Referee()
	proto.ParseFromString(data)
	
	# Instance the ROS msg types to fill them out
	yellow, blue, trama = team_info(), team_info(), referee()
	
	# Translate the team info
	for team, buf in ((yellow, proto.yellow), (blue, proto.blue)):

		team.name = buf.name
		team.score = buf.score
		team.red_cards = buf.red_cards
		team.yellow_card_times = buf.yellow_card_times
		team.yellow_cards = buf.yellow_cards
		team.timeouts = buf.timeouts
		team.timeout_time = buf.timeout_time
		team.goalie = buf.goalie
	
	trama.yellow = yellow
	trama.blue = blue
	
	# Translate the rest
	trama.packet_timestamp = proto.packet_timestamp
	trama.stage = proto.stage
	trama.stage_time_left = proto.stage_time_left
	trama.command = proto.command
	trama.command_counter = proto.command_counter
	trama.command_timestamp = proto.command_timestamp
	
	pub.publish(trama)
	r.sleep()


