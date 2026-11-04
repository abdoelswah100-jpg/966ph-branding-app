package com.motors966.phbranding;

import android.content.ActivityNotFoundException;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.Color;
import android.graphics.pdf.PdfRenderer;
import android.net.Uri;
import android.os.ParcelFileDescriptor;
import android.util.Base64;
import androidx.core.content.FileProvider;
import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import java.io.ByteArrayOutputStream;
import java.io.File;

/** PDF pages to JPEG (Android PdfRenderer) for reading the invoice QR, and opening a file in the phone's viewer. */
@CapacitorPlugin(name = "PdfTools")
public class PdfToolsPlugin extends Plugin {

    private static File fileOf(String path) {
        if (path == null) return null;
        Uri u = Uri.parse(path);
        String p = u.getPath();
        return new File(p != null ? p : path);
    }

    @PluginMethod
    public void render(PluginCall call) {
        final String path = call.getString("path");
        final int max = Math.max(1, call.getInt("pages", 1));
        final int width = Math.max(300, Math.min(2400, call.getInt("width", 1600)));
        new Thread(() -> {
            ParcelFileDescriptor pfd = null;
            PdfRenderer r = null;
            try {
                File f = fileOf(path);
                pfd = ParcelFileDescriptor.open(f, ParcelFileDescriptor.MODE_READ_ONLY);
                r = new PdfRenderer(pfd);
                int n = Math.min(max, r.getPageCount());
                JSArray out = new JSArray();
                for (int i = 0; i < n; i++) {
                    PdfRenderer.Page pg = r.openPage(i);
                    int w = width;
                    int h = (int) Math.max(1, (long) w * pg.getHeight() / Math.max(1, pg.getWidth()));
                    if (h > 4000) {
                        w = (int) Math.max(1, (long) w * 4000 / h);
                        h = 4000;
                    }
                    Bitmap bm = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888);
                    bm.eraseColor(Color.WHITE);
                    pg.render(bm, null, null, PdfRenderer.Page.RENDER_MODE_FOR_DISPLAY);
                    pg.close();
                    ByteArrayOutputStream bo = new ByteArrayOutputStream();
                    bm.compress(Bitmap.CompressFormat.JPEG, 90, bo);
                    bm.recycle();
                    out.put(Base64.encodeToString(bo.toByteArray(), Base64.NO_WRAP));
                }
                JSObject o = new JSObject();
                o.put("count", r.getPageCount());
                o.put("pages", out);
                call.resolve(o);
            } catch (Throwable e) {
                call.reject("render: " + e.getMessage());
            } finally {
                try { if (r != null) r.close(); } catch (Throwable e) {}
                try { if (pfd != null) pfd.close(); } catch (Throwable e) {}
            }
        }).start();
    }

    @PluginMethod
    public void open(PluginCall call) {
        try {
            File f = fileOf(call.getString("path"));
            String mime = call.getString("mime", "application/pdf");
            Uri u = FileProvider.getUriForFile(getContext(), getContext().getPackageName() + ".fileprovider", f);
            Intent i = new Intent(Intent.ACTION_VIEW);
            i.setDataAndType(u, mime);
            i.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            getActivity().startActivity(Intent.createChooser(i, "فتح الملف").addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION));
            call.resolve();
        } catch (ActivityNotFoundException e) {
            call.reject("no viewer");
        } catch (Throwable e) {
            call.reject("open: " + e.getMessage());
        }
    }
}
