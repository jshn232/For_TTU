package main

//ver_0.1  20180521

import (
	"fmt"
	"log"
	"net"
	"os"
	"strings"
	"time"

	"golang.org/x/net/context"
	"google.golang.org/grpc"
	//	pb "google.golang.org/grpc/examples/helloworld/helloworld"
	pb "jshn232/helloworld"  //folder in the $GOPATH/src/

	"google.golang.org/grpc/reflection"
)

//const recvBufLen = 1024 //recv buffer length
const (
	recvBufLen = 1024
	port       = ":50051"
)

// server is used to implement helloworld.GreeterServer.
type server struct{}

//var gRemoteIP []string        //remote ip list
var gmapRemoteIP map[string]chan string //map of remoteip
var gchannelMsg []chan string

func main() {
	gmapRemoteIP = make(map[string]chan string)
	service := "localhost:8990"
	tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
	checkError(err)
	listener, err := net.ListenTCP("tcp4", tcpAddr)
	checkError(err)

	go handleGRPC()
	go handleAccept(listener)

	for {
		time.Sleep(time.Millisecond * 100)
	}
}

//handle gRPC
func handleGRPC() {
	//	var msg string
	lis, err := net.Listen("tcp", port)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}
	s := grpc.NewServer()
	pb.RegisterGreeterServer(s, &server{})
	reflection.Register(s)
	if err := s.Serve(lis); err != nil {
		log.Fatalf("failed to serve: %v", err)
	}
	/*	for {
		for index, ch := range gmapRemoteIP {
			fmt.Println("index:", index)
			fmt.Println("ch:", ch)
			msg = fmt.Sprintf("msg->%s", index)
			ch <- msg
		}
		time.Sleep(time.Second * 2)
	}*/
}

//remote Accpet
func handleAccept(listener net.Listener) {
	for {
		conn, err := listener.Accept()
		if err != nil {
			continue
		}
		go handleClient(conn, make(chan string, 1024))
		time.Sleep(time.Second * 1)
	}
}

//handle client
func handleClient(conn net.Conn, ch chan string) {
	//	conn.SetReadDeadline(time.Now().Add(2 * time.Minute)) // set 2 minutes timeout
	request := make([]byte, recvBufLen) // set maxium request length to 128B to prevent flood attack
	defer conn.Close()                  // close connection before exit
	strIP := conn.RemoteAddr().String()
	fmt.Println("Accept new ip&port from :", strIP)
	appendRemoteIP(strIP, ch)
	getRemoteIP()
	go getChannel(conn, ch)
	for {
		readLen, err := conn.Read(request)

		if err != nil {
			fmt.Println(err)
			deleteRemoteIP(strIP)
			getRemoteIP()
			break
		}
		if readLen <= 0 {
			deleteRemoteIP(strIP)
			getRemoteIP()
			break // connection already closed by client
		} else {
			fmt.Printf("%s", request)
			fmt.Println()
			conn.Write([]byte("hello client!"))
		}
		request = make([]byte, recvBufLen)

		time.Sleep(time.Second * 1)
	}
}

//receive message form channel , send message to client
func getChannel(conn net.Conn, ch chan string) {
	for {
		select {
		case msg := <-ch:
			fmt.Println("receive from channel: ", msg)
			conn.Write([]byte(msg))
		default:
		}
		time.Sleep(time.Millisecond * 100)
	}
}

//check Error
func checkError(err error) {
	if err != nil {
		fmt.Fprintf(os.Stderr, "Fatal error: %s", err.Error())
		os.Exit(1)
	}
}

//get Remote IP map & print
func getRemoteIP() (int, map[string]chan string) {
	fmt.Println("######List of Remote IP######")
	//	for index, ip := range gRemoteIP {
	//		fmt.Printf("No.%02d->%s\n", index, ip)
	//	}
	for ip := range gmapRemoteIP {
		fmt.Printf("IP->%s\n", ip)
	}
	fmt.Println("=============================")
	return len(gmapRemoteIP), gmapRemoteIP
}

//append Remote IP map
func appendRemoteIP(newip string, ch chan string) map[string]chan string {
	//	gRemoteIP = append(gRemoteIP, newip)
	gmapRemoteIP[newip] = ch
	return gmapRemoteIP
}

//delete Remote IP map
func deleteRemoteIP(oldip string) map[string]chan string {
	delete(gmapRemoteIP, oldip)
	return gmapRemoteIP
}

// SayHello implements helloworld.GreeterServer
func (s *server) SayHello(ctx context.Context, in *pb.HelloRequest) (*pb.HelloReply, error) {
	for ip, ch := range gmapRemoteIP {
		sStr := strings.SplitN(ip, ":", 2)
		IP := sStr[0]
		if IP == in.Ip {
			ch <- in.Msg
		}
	}
	return &pb.HelloReply{Message: "Hello " + in.Msg}, nil
}
