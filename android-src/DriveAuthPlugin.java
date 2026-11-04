package com.motors966.phbranding;

import android.app.PendingIntent;
import androidx.activity.result.ActivityResult;
import androidx.activity.result.ActivityResultLauncher;
import androidx.activity.result.IntentSenderRequest;
import androidx.activity.result.contract.ActivityResultContracts;
import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.google.android.gms.auth.GoogleAuthUtil;
import com.google.android.gms.auth.api.identity.AuthorizationRequest;
import com.google.android.gms.auth.api.identity.AuthorizationResult;
import com.google.android.gms.auth.api.identity.Identity;
import com.google.android.gms.common.api.Scope;
import java.util.Collections;

/** Google Drive access (drive.file only) through Google Play services Authorization API. No secret, no server. */
@CapacitorPlugin(name = "DriveAuth")
public class DriveAuthPlugin extends Plugin {

    private static final String SCOPE = "https://www.googleapis.com/auth/drive.file";
    private PluginCall pending;
    private ActivityResultLauncher<IntentSenderRequest> launcher;

    @Override
    public void load() {
        launcher = getActivity().registerForActivityResult(new ActivityResultContracts.StartIntentSenderForResult(), this::onResult);
    }

    /** interactive=false: returns {need:true} when Google wants the user (first time, weekly in testing mode). */
    @PluginMethod
    public void authorize(PluginCall call) {
        final boolean interactive = Boolean.TRUE.equals(call.getBoolean("interactive", false));
        AuthorizationRequest req = AuthorizationRequest.builder().setRequestedScopes(Collections.singletonList(new Scope(SCOPE))).build();
        Identity.getAuthorizationClient(getActivity())
            .authorize(req)
            .addOnSuccessListener(r -> {
                if (r.hasResolution()) {
                    if (!interactive) {
                        JSObject o = new JSObject();
                        o.put("need", true);
                        call.resolve(o);
                        return;
                    }
                    PendingIntent pi = r.getPendingIntent();
                    if (pi == null) {
                        call.reject("no consent screen");
                        return;
                    }
                    if (pending != null) pending.reject("replaced");
                    pending = call;
                    try {
                        launcher.launch(new IntentSenderRequest.Builder(pi.getIntentSender()).build());
                    } catch (Exception e) {
                        pending = null;
                        call.reject("launch: " + e.getMessage());
                    }
                } else {
                    ok(call, r);
                }
            })
            .addOnFailureListener(e -> call.reject("authorize: " + e.getMessage()));
    }

    private void ok(PluginCall c, AuthorizationResult r) {
        if (r.getAccessToken() == null) {
            c.reject("no access token");
            return;
        }
        JSObject o = new JSObject();
        o.put("token", r.getAccessToken());
        JSArray g = new JSArray();
        for (String s : r.getGrantedScopes()) g.put(s);
        o.put("scopes", g);
        c.resolve(o);
    }

    private void onResult(ActivityResult res) {
        PluginCall c = pending;
        pending = null;
        if (c == null) return;
        try {
            AuthorizationResult r = Identity.getAuthorizationClient(getActivity()).getAuthorizationResultFromIntent(res.getData());
            ok(c, r);
        } catch (Exception e) {
            c.reject("cancelled");
        }
    }

    /** Drops a token Google refused (401) so the next authorize gets a fresh one. */
    @PluginMethod
    public void clearToken(PluginCall call) {
        final String t = call.getString("token", "");
        new Thread(() -> {
            try {
                if (t != null && !t.isEmpty()) GoogleAuthUtil.clearToken(getContext(), t);
                call.resolve();
            } catch (Exception e) {
                call.reject("clear: " + e.getMessage());
            }
        }).start();
    }
}
