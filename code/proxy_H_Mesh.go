package main

//HY-Mesh 拨号代理工具  20180930 scy
import (
	"fmt"
	"io"
	"net"
	"os"
	"strings"
	"sync"
	"time"
)

var lock sync.Mutex
var trueList [4][]string
var ip [4]string
var list [4]string

func main() {
	ip[0] = "172.30.32.177:9090"
	list[0] = "172.18.119.69:3105"

	ip[1] = "172.30.32.177:9091"
	list[1] = "172.103.19.184:3105"

	ip[2] = "172.30.32.177:9092"
	list[2] = "172.107.39.254:3105"

	ip[3] = "172.30.32.177:9093"
	list[3] = "172.107.40.1:3105"
	//	flag.StringVar(&ip[0], "l", "172.30.32.177:9090", "-l=0.0.0.0:9897 指定服务监听的端口")
	//	flag.StringVar(&list[0], "d", "172.18.119.69:3105", "-d=127.0.0.1:1789,127.0.0.1:1788 指定后端的IP和端口,多个用','隔开")

	//	flag.StringVar(&ip[1], "l", "172.30.32.177:9091", "-l=0.0.0.0:9897 指定服务监听的端口")
	//	flag.StringVar(&list[1], "d", "172.103.19.184:3105", "-d=127.0.0.1:1789,127.0.0.1:1788 指定后端的IP和端口,多个用','隔开")

	//	flag.StringVar(&ip[2], "l", "172.30.32.177:9092", "-l=0.0.0.0:9897 指定服务监听的端口")
	//	flag.StringVar(&list[2], "d", "172.107.39.254:3105", "-d=127.0.0.1:1789,127.0.0.1:1788 指定后端的IP和端口,多个用','隔开")

	//	flag.StringVar(&ip[3], "l", "172.30.32.177:9093", "-l=0.0.0.0:9897 指定服务监听的端口")
	//	flag.StringVar(&list[3], "d", "172.107.40.1:3105", "-d=127.0.0.1:1789,127.0.0.1:1788 指定后端的IP和端口,多个用','隔开")
	//	flag.Parse()
	for index := 0; index < 4; index++ {
		trueList[index] = strings.Split(list[index], ",")
		if len(trueList[index]) <= 0 {
			fmt.Println("后端IP和端口不能空,或者无效")
			os.Exit(1)
		}
		go func(Num int) {
			lis, err := net.Listen("tcp", ip[Num])
			if err != nil {
				fmt.Println(err)
				return
			}
			defer lis.Close()
			for {
				conn, err := lis.Accept()
				if err != nil {
					fmt.Println("建立连接错误:%v\n", err)
					continue
				}
				fmt.Println(conn.RemoteAddr(), conn.LocalAddr())
				go handle(conn, Num)
			}
		}(index)

	}
	//	go server(0)
	//	go server(1)
	//	go server(2)
	//	go server(3)

	for {
		time.Sleep(time.Millisecond * 100)
	}
}
func server(Num int) {
	lis, err := net.Listen("tcp", ip[Num])
	if err != nil {
		fmt.Println(err)
		return
	}
	defer lis.Close()
	for {
		conn, err := lis.Accept()
		if err != nil {
			fmt.Println("建立连接错误:%v\n", err)
			continue
		}
		fmt.Println(conn.RemoteAddr(), conn.LocalAddr())
		go handle(conn, Num)
	}
}
func handle(sconn net.Conn, Num int) {
	defer sconn.Close()
	ip, ok := getIP(Num)
	if !ok {
		return
	}
	dconn, err := net.Dial("tcp", ip)
	if err != nil {
		fmt.Printf("连接%v失败:%v\n", ip, err)
		return
	}
	ExitChan := make(chan bool, 1)
	go func(sconn net.Conn, dconn net.Conn, Exit chan bool) {
		_, err := io.Copy(dconn, sconn)
		fmt.Printf("往%v发送数据失败:%v\n", ip, err)
		ExitChan <- true
	}(sconn, dconn, ExitChan)
	go func(sconn net.Conn, dconn net.Conn, Exit chan bool) {
		_, err := io.Copy(sconn, dconn)
		fmt.Printf("从%v接收数据失败:%v\n", ip, err)
		ExitChan <- true
	}(sconn, dconn, ExitChan)
	<-ExitChan
	dconn.Close()
}
func getIP(Num int) (string, bool) {
	lock.Lock()
	defer lock.Unlock()
	if len(trueList[Num]) < 1 {
		return "", false
	}
	ip := trueList[Num][0]
	//	trueList = append(trueList[Num][1:], ip)
	return ip, true
}
