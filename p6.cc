
#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include "ns3/flow-monitor-module.h"

using namespace ns3;

int
main (int argc, char *argv[])
{

  uint32_t maxBytes = 0; // 0 means "send unlimited" (until app stops)
  double simStop = 10.0; // seconds
  std::string dataRate = "500kbps";
  std::string delay = "5ms";
  uint16_t port = 9;

  CommandLine cmd;
  cmd.AddValue ("MaxBytes", "Max bytes to send (0 for unlimited)", maxBytes);
  cmd.AddValue ("Stop", "Simulation stop time (s)", simStop);
  cmd.AddValue ("DataRate", "Data rate for point-to-point link", dataRate);
  cmd.AddValue ("Delay", "Delay for point-to-point link", delay);
  cmd.Parse (argc, argv);

  // Create nodes
  NodeContainer nodes;
  nodes.Create (2);

  // Create point-to-point link with attributes
  PointToPointHelper pointToPoint;
  pointToPoint.SetDeviceAttribute ("DataRate", StringValue (dataRate));
  pointToPoint.SetChannelAttribute ("Delay", StringValue (delay));

  // Install devices on nodes
  NetDeviceContainer devices = pointToPoint.Install (nodes);


  InternetStackHelper stack;
  stack.Install (nodes);


  Ipv4AddressHelper ipv4;
  ipv4.SetBase ("10.1.1.0", "255.255.255.0");
  Ipv4InterfaceContainer interfaces = ipv4.Assign (devices);


  Address sinkAddress (InetSocketAddress (interfaces.GetAddress (1), port));
  BulkSendHelper source ("ns3::TcpSocketFactory", sinkAddress);
  source.SetAttribute ("MaxBytes", UintegerValue (maxBytes)); // 0 means unlimited

  ApplicationContainer sourceApps = source.Install (nodes.Get (0));
  sourceApps.Start (Seconds (0.0));
  sourceApps.Stop (Seconds (simStop));


  PacketSinkHelper sinkHelper ("ns3::TcpSocketFactory",
                               InetSocketAddress (Ipv4Address::GetAny (), port));
  ApplicationContainer sinkApps = sinkHelper.Install (nodes.Get (1));
  sinkApps.Start (Seconds (0.0));
  sinkApps.Stop (Seconds (simStop));


  AsciiTraceHelper ascii;
  pointToPoint.EnableAsciiAll (ascii.CreateFileStream ("p6-trace.tr"));


  FlowMonitorHelper flowmonHelper;
  Ptr<FlowMonitor> monitor = flowmonHelper.InstallAll ();


  Simulator::Stop (Seconds (simStop));
  Simulator::Run ();

  monitor->SerializeToXmlFile ("p6-tcp-flowmonitor.xml", true, true);

  Ptr<PacketSink> sink1 = DynamicCast<PacketSink> (sinkApps.Get (0));
  if (sink1)
    {
      std::cout << "Total Bytes Received: " << sink1->GetTotalRx () << std::endl;
    }
  else
    {
      std::cout << "ERROR: Could not get pointer to PacketSink." << std::endl;
    }

  Simulator::Destroy ();
  return 0;
}
