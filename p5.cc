#include <string>
#include <fstream>
#include "ns3/core-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/internet-module.h"
#include "ns3/applications-module.h"
#include "ns3/network-module.h"
#include "ns3/packet-sink.h"
//Output is .tr file -cmd : java -jar tracematrics.jar(file path)

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("TcpBulkSendExample");

int
main(int argc, char *argv[])
{
  bool tracing = true;
  uint32_t maxBytes = 0;

  NodeContainer nodes;
  nodes.Create(2);


  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute("DataRate", StringValue("500Kbps"));
  pointToPoint.SetChannelAttribute("Delay", StringValue("5ms"));
  NetDeviceContainer devices;
  devices = pointToPoint.Install(nodes);

  InternetStackHelper internet;
  internet.Install(nodes);

  Ipv4AddressHelper ipv4;
  ipv4.SetBase("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer i = ipv4.Assign(devices);

  uint16_t port = 9; 
  BulkSendHelper source("ns3::TcpSocketFactory", InetSocketAddress(i.GetAddress(1), port));
  source.SetAttribute("MaxBytes", UintegerValue(maxBytes));
  ApplicationContainer sourceApps = source.Install(nodes.Get(0));
  sourceApps.Start(Seconds(0.0));
  sourceApps.Stop(Seconds(10.0));

  
  PacketSinkHelper sink("ns3::TcpSocketFactory", InetSocketAddress(Ipv4Address::GetAny(), port));
  ApplicationContainer sinkApps = sink.Install(nodes.Get(1));
  sinkApps.Start(Seconds(0.0));
  sinkApps.Stop(Seconds(10.0));


  if (tracing)
  {
    AsciiTraceHelper ascii;
    Ptr<OutputStreamWrapper> stream = ascii.CreateFileStream("tcp-bulk-send.tr");
    pointToPoint.EnableAsciiAll(stream);
    pointToPoint.EnablePcapAll("tcp-bulk-send", false);
  }

  Simulator::Stop(Seconds(10.0));
  Simulator::Run();

  Ptr<Application> app = sinkApps.Get(0);
  Ptr<PacketSink> sink1 = DynamicCast<PacketSink>(app);
  std::cout << "Total Bytes Received: " << sink1->GetTotalRx() << std::endl;


  Simulator::Destroy();

  return 0; 
}
