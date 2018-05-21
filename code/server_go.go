package main

//ver_0.1  20180521

import (
	"fmt"
	"net"
	"os"
	"time"
)

const recvBufLen = 1024 //recv buffer length

//var gRemoteIP []string        //remote ip list
var gmapRemoteIP map[string]chan string //map of remoteip
var gchannelMsg []chan string

func main() {
	gmapRemoteIP = make(map[string]chan string)
	service := "localhost:8990"
	tcpAddr, err := net.ResolveTCPAddr("tcp4", service)
	checkError(err)
	listener, err := net.ListenTCP("tcp", tcpAddr)
	checkError(err)

	go handleGRPC()
	go handleAccept(listener)

	for {
		time.Sleep(time.Millisecond * 100)
	}
}

//处理gRPC消息
func handleGRPC() {
	var msg string
	for {
		for index, ch := range gmapRemoteIP {
			fmt.Println("index:", index)
			fmt.Println("ch:", ch)
			msg = fmt.Sprintf("msg->%s", index)
			ch <- msg
		}
		time.Sleep(time.Second * 2)
	}
}

//客户端接收
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

//客户端处理
func handleClient(conn net.Conn, ch chan string) {
	conn.SetReadDeadline(time.Now().Add(2 * time.Minute)) // set 2 minutes timeout
	request := make([]byte, recvBufLen)                   // set maxium request length to 128B to prevent flood attack
	defer conn.Close()                                    // close connection before exit
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

//从channel获取消息，转发至客户端
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
