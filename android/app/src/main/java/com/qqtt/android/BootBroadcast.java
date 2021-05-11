package com.qqtt.android;

import android.content.Context;
import android.content.Intent;

import android.content.BroadcastReceiver;

public class BootBroadcast extends BroadcastReceiver {

    @Override
    public void onReceive(Context context, Intent mintent) {
        System.out.println("hehe");
        Intent service = new Intent(context, BackService.class);
        System.out.println(context);
        System.out.println(service);
        context.startService(service);
        context.stopService(service);
/*
        if (Intent.ACTION_BOOT_COMPLETED.equals(mintent.getAction())) {
            System.out.println("start broadcast");
            Intent service = new Intent(context, BackService.class);
            context.startService(service);
        }

 */
    }
}
