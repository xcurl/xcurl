// Module Includes
#include "ns3/core-module.h"
// Core functionalities (Time, Simulator, Logging)
#include "ns3/network-module.h"
// Network components (Node, NetDevice, Channel)
#include "ns3/internet-module.h" // Internet stack (TCP, UDP, IP)
#include "ns3/point-to-point-module.h" // Point-to-Point link helpers
#include "ns3/applications-module.h" // Application helpers (Echo Server/Client)
#include "ns3/netanim-module.h"

using namespace ns3;

NS_LOG_COMPONENT_DEFINE ("FirstScriptExample");

int
main (int argc, char *argv[])
{
LogComponentEnable("UdpEchoClientApplication",LOG_LEVEL_INFO);
LogComponentEnable("UdpEchoServerApplication",LOG_LEVEL_INFO);

NodeContainer nodes;
nodes.Create(2);

PointToPointHelper p2p;
p2p.SetDeviceAttribute("DataRate",StringValue("5Mbps"));
p2p.SetChannelAttribute("Delay",StringValue("2ms"));

NetDeviceContainer devices;
devices = p2p.Install(nodes);

InternetStackHelper stack;
stack.Install(nodes);

Ipv4AddressHelper add;
add.SetBase("10.1.1.0","255.255.255.0");
Ipv4InterfaceContainer interfaces = add.Assign(devices);

UdpEchoServerHelper echoserver(9);
ApplicationContainer serverApps = echoserver.Install(nodes.Get(1));
serverApps.Start(Seconds(1.0));
serverApps.Stop(Seconds(10.0));

UdpEchoClientHelper echoclient(interfaces.GetAddress(1),9);
echoclient.SetAttribute("MaxPackets",UintegerValue(1));
echoclient.SetAttribute("Interval",TimeValue(Seconds(1.0)));
echoclient.SetAttribute("PacketSize",UintegerValue(1014));
ApplicationContainer clientapps = echoclient.Install(nodes.Get(0));
clientapps.Start(Seconds(2.0));
clientapps.Stop(Seconds(10.0));

AnimationInterface anim("Prg2.xml");
anim.SetConstantPosition(nodes.Get(0),10.0,10.0);
anim.SetConstantPosition(nodes.Get(1),20.0,30.0);


Simulator::Run();
Simulator::Destroy();
return 0;
}
