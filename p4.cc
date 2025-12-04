#include "ns3/core-module.h"
#include "ns3/network-module.h"
#include "ns3/netanim-module.h"
#include "ns3/internet-module.h"
#include "ns3/point-to-point-module.h"
#include "ns3/applications-module.h"
#include <vector>
#include <cmath>

using namespace ns3;

NS_LOG_COMPONENT_DEFINE("Start123");

int main(int argc, char *argv[])
{

    Config::SetDefault("ns3::OnOffApplication::PacketSize", UintegerValue(137));
    Config::SetDefault("ns3::OnOffApplication::DataRate", StringValue("14kb/s"));

    uint32_t nSpokes = 8;
    std::string animFile1 = "star-animation1.xml";

    CommandLine cmd;
    cmd.AddValue("nSpokes", "Number of nodes to place in the star", nSpokes);
    cmd.AddValue("animFile1", "File Name for Animation Output", animFile1);
    cmd.Parse(argc, argv);

    NS_LOG_INFO("Build star topology.");
    Ptr<Node> hub = CreateObject<Node>();
    NodeContainer spokes;
    spokes.Create(nSpokes);
    NodeContainer allNodes(hub);
    allNodes.Add(spokes);

    // Set up point-to-point connections between hub and each spoke
    PointToPointHelper pointToPoint;
    pointToPoint.SetDeviceAttribute("DataRate", StringValue("5Mbps"));
    pointToPoint.SetChannelAttribute("Delay", StringValue("2ms"));

    std::vector<NetDeviceContainer> devices(nSpokes); // Vector to store devices for each link
    for (uint32_t i = 0; i < nSpokes; ++i)
    {
        devices[i] = pointToPoint.Install(hub, spokes.Get(i));
    }

    NS_LOG_INFO("Install internet stack on all nodes.");
    InternetStackHelper internet;
    internet.Install(allNodes);

    NS_LOG_INFO("Assign IP Addresses.");
    Ipv4AddressHelper ipv4;
    ipv4.SetBase("10.1.1.0", "255.255.255.0");
    std::vector<Ipv4InterfaceContainer> interfaces(nSpokes);
    for (uint32_t i = 0; i < nSpokes; ++i)
    {
        interfaces[i] = ipv4.Assign(devices[i]);
        ipv4.NewNetwork(); // Increment network for the next spoke
    }

    NS_LOG_INFO("Create applications.");
    //
    // Create a packet sink on the star "hub" to receive packets.
    //
    uint16_t port = 50000;
    Address hubLocalAddress(InetSocketAddress(Ipv4Address::GetAny(), port));
    PacketSinkHelper packetSinkHelper("ns3::TcpSocketFactory", hubLocalAddress);
    ApplicationContainer hubApp = packetSinkHelper.Install(hub);
    hubApp.Start(Seconds(1.0));
    hubApp.Stop(Seconds(10.0));


    OnOffHelper onOffHelper("ns3::TcpSocketFactory", Address());
    onOffHelper.SetAttribute("OnTime", StringValue("ns3::ConstantRandomVariable[Constant=1]"));
    onOffHelper.SetAttribute("OffTime", StringValue("ns3::ConstantRandomVariable[Constant=0]"));
    ApplicationContainer spokeApps;
    for (uint32_t i = 0; i < nSpokes; ++i)
    {
        AddressValue remoteAddress(InetSocketAddress(interfaces[i].GetAddress(0), port)); // Hub's IP address
        onOffHelper.SetAttribute("Remote", remoteAddress);
        spokeApps.Add(onOffHelper.Install(spokes.Get(i)));
    }
    spokeApps.Start(Seconds(1.0));
    spokeApps.Stop(Seconds(10.0));

    NS_LOG_INFO("Enable static global routing.");
    Ipv4GlobalRoutingHelper::PopulateRoutingTables();

    NS_LOG_INFO("Enable pcap tracing.");
    pointToPoint.EnablePcapAll("star123");

    // Set positions for animation (mimic star topology layout)
    AnimationInterface anim(animFile1);
    anim.SetConstantPosition(hub, 50, 50); // Hub at center
    double angleStep = 2 * M_PI / nSpokes;
    double radius = 40.0; // Radius for spoke nodes
    for (uint32_t i = 0; i < nSpokes; ++i)
    {
        double angle = i * angleStep;
        double x = 50 + radius * cos(angle);
        double y = 50 + radius * sin(angle);
        anim.SetConstantPosition(spokes.Get(i), x, y);
    }

    NS_LOG_INFO("Run Simulation.");
    Simulator::Run();
    Simulator::Destroy();
    NS_LOG_INFO("Done.");

    return 0;
}
