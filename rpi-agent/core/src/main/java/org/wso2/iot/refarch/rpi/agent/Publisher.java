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

import org.eclipse.paho.client.mqttv3.MqttException;
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

/**
 * Publisher class in the Raspberry Pi IoT agent
 */
public class Publisher {
    private static final int DEFAULT_DATA_PIN_NUMBER = 15;
    private static final int DEFAULT_UPDATE_INTERVAL = 10;
    private DHTSensor dhtSensor;
    private MQTTClient mqttClient;
    private MQTTBrokerConnectionConfig mqttBrokerConnectionConfig;
    private Agent agent;
    public Publisher(int dataPinNumber) {
        dhtSensor = new DHTSensor(DHTSensorType.DHT11, dataPinNumber);
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
        String clientId = "R-Pi-Publisher";
        String topicName = "wso2iot";
        mqttClient = new MQTTClient(mqttBrokerConnectionConfig,clientId,topicName);
        agent = new Agent();
    }

    public static void main(String[] args) {
        int dataPinNumber = DEFAULT_DATA_PIN_NUMBER;
        int updateInterval = DEFAULT_UPDATE_INTERVAL;
        if(args.length > 1 && args[1] != null) {
            updateInterval = Integer.parseInt(args[1]);
        } else if (args.length > 2 && args[2] != null) {
            dataPinNumber = Integer.parseInt(args[2]);
        }

        Publisher pub = new Publisher(dataPinNumber);
        if (args.length > 0 && args[0] != null) {
            try {
                pub.agent.register(args[0]);
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        pub.start(updateInterval);
    }

    private void start(int updateInterval) {
        ScheduledExecutorService dhtReaderScheduler = Executors.newScheduledThreadPool(1);
        dhtReaderScheduler.scheduleWithFixedDelay(new MonitoringTask(dhtSensor), 0, updateInterval, TimeUnit.SECONDS);
    }
    public class MonitoringTask implements Runnable {
        private DHTSensor dhtSensor;

        public MonitoringTask(DHTSensor dhtSensor) {
            this.dhtSensor = dhtSensor;
        }

        @Override
        public void run() {
            dhtSensor.read();
            float temperature = dhtSensor.getTemperature(false);
            int humidity = dhtSensor.getHumidity();
            JSONObject payload = generatePayload(humidity, temperature);
            try {
                String message = "Temperature:" + Float.toString(temperature);
                String humidityMsg = "Humidity:" + Integer.toString(humidity);
                mqttClient.publish(1,message.getBytes());
//                mqttClient.publish(1,humidityMsg.getBytes());
                JSONObject infoObject = agent.createInfoObject();
                //Inserting the sensors payload to info object
                infoObject.put("sensors", payload);
                agent.sendPayload(infoObject);
            } catch (MqttException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            } catch (ExecutionException e) {
                e.printStackTrace();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
    public JSONObject generatePayload(int humdity, float temperature){
        JSONObject payload = new JSONObject();
        payload.put("humidity", humdity);
        payload.put("temperature", temperature);
        return payload;
    }
}
