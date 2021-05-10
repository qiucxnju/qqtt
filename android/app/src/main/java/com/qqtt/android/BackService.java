package com.qqtt.android;


import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import android.app.ActivityManager;
import android.app.AlarmManager;
import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.app.Service;
import android.content.Intent;
import android.content.SharedPreferences;
import android.graphics.Color;
import android.location.Location;
import android.location.LocationManager;
import android.os.IBinder;

public class BackService extends Service {
    String base_url = "http://www.qqttgroup.com/findpapa/setLocation";
    public void sendLocation(String cookie, double lng, double lat) {
        HttpURLConnection conn=null;
        try {
        URL url = new URL(base_url + "?lng=" + lng + "&lat=" + lat);
         conn = (HttpURLConnection)url.openConnection();
        conn.setRequestProperty("Cookie", cookie);
            conn.setConnectTimeout(5000);
            conn.setRequestMethod("GET");
        if (HttpURLConnection.HTTP_OK == conn.getResponseCode()) {
            System.out.println("发送成功");
        }else{
            System.out.println("发送失败");
        }
        } catch (Exception e) {
            e.printStackTrace();
        }
        finally {
            conn.disconnect();
        }
        return ;
    }
    public String getCookie(){
        System.out.println("timer");
        SharedPreferences pref = getSharedPreferences("data",MODE_PRIVATE);
        String cookieStr = pref.getString("cookie", "");
        System.out.println(cookieStr);
        return cookieStr;
    }
    public Location  getLocation(){
        LocationManager m_locationManager = (LocationManager) getSystemService(LOCATION_SERVICE);
        String m_provider = null;
        //获取当前可用的位置控制器
        List<String> list = m_locationManager.getProviders(true);
        if (list.contains(LocationManager.GPS_PROVIDER)) {
            //是否为GPS位置控制器
            m_provider = LocationManager.NETWORK_PROVIDER;//NETWORK_PROVIDER GPS_PROVIDER
            System.out.println("is GPS");
        }
        else if (list.contains(LocationManager.NETWORK_PROVIDER)) {
            //是否为网络位置控制器
            m_provider = LocationManager.NETWORK_PROVIDER;
            System.out.println("is network");
        }
        if(m_provider != null) {
            Location location = m_locationManager.getLastKnownLocation(m_provider);
            System.out.println(location.toString());
            return location;
        }else {

            System.out.println("no location");
            return null;
        }
    }
    Timer timer = new Timer();
    TimerTask task = new TimerTask() {
        @Override
        public void run(){
            String cookie = getCookie();
            Location location = getLocation();
            if (location == null)
                return;
            double lat = location.getLatitude();
            double lng = location.getLongitude();
            System.out.println(lat);
            System.out.println(lng);
            sendLocation(cookie, lng, lat);
        }
    };
    /** 标识服务如果被杀死之后的行为 */
    int mStartMode;

    private boolean mRunning;

    /** 绑定的客户端接口 */
    IBinder mBinder;

    /** 标识是否可以使用onRebind */
    boolean mAllowRebind;

    /** 当服务被创建时调用. */
    @Override
    public void onCreate() {
        frontService();
    }

    /** 调用startService()启动服务时回调 */
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        if (!mRunning) {
            mRunning = true;
        }else{
            return 0;
        }
        System.out.println("service start");
        timer.schedule(task, 0, 10000);

        return START_STICKY;
    }

    /** 通过bindService()绑定到服务的客户端 */
    @Override
    public IBinder onBind(Intent intent) {
        return mBinder;
    }

    /** 通过unbindService()解除所有客户端绑定时调用 */
    @Override
    public boolean onUnbind(Intent intent) {
        return mAllowRebind;
    }

    /** 通过bindService()将客户端绑定到服务时调用*/
    @Override
    public void onRebind(Intent intent) {

    }

    /** 服务不再有用且将要被销毁时调用 */
    @Override
    public void onDestroy() {
        timer.cancel();
        System.out.println("service destroy");

    }
    String CHANNEL_ONE_ID = "com.qqttgroup.com";
    String CHANNEL_ONE_NAME = "com.qqttgroup.com";
    private void frontService() {
        NotificationChannel notificationChannel;
//进行8.0的判断
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            notificationChannel= new NotificationChannel(CHANNEL_ONE_ID,
                    CHANNEL_ONE_NAME, NotificationManager.IMPORTANCE_HIGH);
            notificationChannel.enableLights(true);
            notificationChannel.setLightColor(Color.RED);
            notificationChannel.setShowBadge(true);
            notificationChannel.setLockscreenVisibility(Notification.VISIBILITY_PUBLIC);
            NotificationManager manager= (NotificationManager) getSystemService(NOTIFICATION_SERVICE);
            if (manager != null) {
                manager.createNotificationChannel(notificationChannel);
            }
        }
        Intent intent = new Intent(this, MainActivity.class);
        PendingIntent pendingIntent= PendingIntent.getActivity(this, 0, intent, 0);
        Notification notification= new Notification.Builder(this, CHANNEL_ONE_ID).setChannelId(CHANNEL_ONE_ID)
                .setTicker("Nature")
                .setSmallIcon(R.mipmap.ic_launcher)
                .setContentTitle("这是一个测试标题")
                .setContentIntent(pendingIntent)
                .setContentText("这是一个测试内容")
                .build();
        notification.flags|= Notification.FLAG_NO_CLEAR;
        startForeground(1, notification);
        //发送一般通知
       // manager.notify(1,builder.build());
    }
}
