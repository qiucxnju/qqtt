package com.qqtt.android;


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

import com.baidu.location.BDAbstractLocationListener;
import com.baidu.location.BDLocation;
import com.baidu.location.LocationClient;
import com.baidu.location.LocationClientOption;

import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

public class BackService extends Service {
    String base_url = "http://www.qqttgroup.com/findpapa/setLocation";
    public  class  SendThread  extends  Thread
    {
        HttpURLConnection conn = null;
        public  String cookie;
        public double lng, lat;
        public  SendThread(String cookie, double lng, double lat)
        {
            this .cookie = cookie;
            this.lng = lng;
            this.lat = lat;
        }
        public  void  run()
        {
            try {
            URL url = new URL(base_url + "?lng=" + lng + "&lat=" + lat);
            conn = (HttpURLConnection) url.openConnection();
            conn.setRequestProperty("Cookie", cookie);
            conn.setConnectTimeout(5000);
            conn.setRequestMethod("GET");
            if (HttpURLConnection.HTTP_OK == conn.getResponseCode()) {
                System.out.println("发送成功");
            } else {
                System.out.println("发送失败");
            }
        } catch (Exception e) {
            e.printStackTrace();
        } finally {
            conn.disconnect();
        }
            return;
        }
    }
    public void sendLocation(String cookie, double lng, double lat) {
        Thread thread = new SendThread(cookie,lng, lat);
        thread.start();
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
    LocationClient locationClient;
    private void initLocationOption() {
        System.out.println("init location option");
//定位服务的客户端。宿主程序在客户端声明此类，并调用，目前只支持在主线程中启动
        locationClient = new LocationClient(getApplicationContext());
//声明LocationClient类实例并配置定位参数
        LocationClientOption locationOption = new LocationClientOption();
        MyLocationListener myLocationListener = new MyLocationListener();
//注册监听函数
        locationClient.registerLocationListener(myLocationListener);
//可选，默认高精度，设置定位模式，高精度，低功耗，仅设备
        locationOption.setLocationMode(LocationClientOption.LocationMode.Hight_Accuracy);
//可选，默认gcj02，设置返回的定位结果坐标系，如果配合百度地图使用，建议设置为bd09ll;
        locationOption.setCoorType("BD09LL");
//可选，默认0，即仅定位一次，设置发起连续定位请求的间隔需要大于等于1000ms才是有效的
        locationOption.setScanSpan(5 * 60 * 1000);
//可选，默认true，定位SDK内部是一个SERVICE，并放到了独立进程，设置是否在stop的时候杀死这个进程，默认不杀死
        locationOption.setIgnoreKillProcess(true);
//可选，默认false，设置是否开启Gps定位
        locationOption.setOpenGps(true);
//需将配置好的LocationClientOption对象，通过setLocOption方法传递给LocationClient对象使用
        locationClient.setLocOption(locationOption);
//开始定位
        locationClient.start();
    }
    class MyLocationListener extends BDAbstractLocationListener {
        @Override
        public void onReceiveLocation(BDLocation location){
            //此处的BDLocation为定位结果信息类，通过它的各种get方法可获取定位相关的全部结果
            //以下只列举部分获取经纬度相关（常用）的结果信息
            //更多结果信息获取说明，请参照类参考中BDLocation类中的说明

            //获取纬度信息
            double latitude = location.getLatitude();
            //获取经度信息
            double longitude = location.getLongitude();
            //获取定位精度，默认值为0.0f
            float radius = location.getRadius();
            //获取经纬度坐标类型，以LocationClientOption中设置过的坐标类型为准
            String coorType = location.getCoorType();
            //获取定位类型、定位错误返回码，具体信息可参照类参考中BDLocation类中的说明
            int errorCode = location.getLocType();
            System.out.println(errorCode);

            String cookie = getCookie();


            System.out.println(longitude);
            System.out.println(latitude);
            if((longitude > 50)&&(longitude < 200))
                sendLocation(cookie, longitude, latitude);
        }
    }
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
        System.out.println("service create");
    }

    /** 调用startService()启动服务时回调 */
    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        System.out.println("service onStartCommand");
        if (!mRunning) {
            mRunning = true;
        }else{
            return 0;
        }
        System.out.println("service start");
        initLocationOption();

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
        locationClient.stop();
        System.out.println("service destroy");
    }
}
