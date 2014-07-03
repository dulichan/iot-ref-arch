/*
 *  Copyright (c) 2005-2014, WSO2 Inc. (http://www.wso2.org) All Rights Reserved.
 *
 *  WSO2 Inc. licenses this file to you under the Apache License,
 *  Version 2.0 (the "License"); you may not use this file except
 *  in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *  http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing,
 *  software distributed under the License is distributed on an
 *  "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 *  KIND, either express or implied.  See the License for the
 *  specific language governing permissions and limitations
 *  under the License.
 *
 */
package org.wso2.iot.refarch.rpi.agent;

import com.pi4j.io.gpio.GpioController;
import com.pi4j.io.gpio.GpioFactory;
import com.pi4j.io.gpio.GpioPinDigitalOutput;
import com.pi4j.io.gpio.RaspiPin;
import org.json.simple.JSONObject;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;
import java.util.concurrent.ExecutionException;
import java.util.concurrent.Executors;
import java.util.concurrent.ScheduledExecutorService;
import java.util.concurrent.TimeUnit;

public class Receiver{
    private final Agent agent;
    private MQTTClient mqttClient;
    private MQTTBrokerConnectionConfig mqttBrokerConnectionConfig;
    final GpioController gpio;
    final GpioPinDigitalOutput pin;
    {
        gpio = GpioFactory.getInstance();
        pin = gpio.provisionDigitalOutputPin(RaspiPin.GPIO_00, "Relay");
    }
    //17
    public Receiver() {
        InputStream is = null;
        try {
            is = new FileInputStream("config.properties");
            Properties properties = new Properties();
            properties.load(is);
            System.out.println("Server ip "+properties.getProperty("mqttpath"));
            RpiAgentConstants.MQTT_AGENT_HOSTNAME =  properties.getProperty("mqttpath");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }
        mqttBrokerConnectionConfig = new MQTTBrokerConnectionConfig(RpiAgentConstants.MQTT_AGENT_HOSTNAME,"1883");
        String clientId = "R-Pi-Receiver";
        String topicName = "iot/demo";
        mqttClient = new MQTTClient(mqttBrokerConnectionConfig,clientId,topicName, this);
        agent = new Agent();
    }

    private void start() {
        ScheduledExecutorService dhtReaderScheduler = Executors.newScheduledThreadPool(1);
        dhtReaderScheduler.scheduleWithFixedDelay(new MonitoringTask(), 0, 10, TimeUnit.SECONDS);
    }
    public class MonitoringTask implements Runnable {

        public MonitoringTask() {
        }

        @Override
        public void run() {

            try {
                JSONObject infoObject = agent.createInfoObject();
                // If true - Fan is on. If false Fan is off.
                infoObject.put("actuator", pin.isHigh());
                agent.sendPayload(infoObject);
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
    public static void main(String[] args) {
        Receiver r = new Receiver();
        if (args.length > 0 && args[0] != null) {
            try {
                r.agent.register(args[0]);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        r.start();
    }
    public void run(String message){
        System.out.println("Message received "+message);
        if(message.equals("ON")){
           pin.high();
        }else if(message.equals("OFF")){
            pin.low();
        }
    }
}
