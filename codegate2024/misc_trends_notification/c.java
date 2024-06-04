// Decompiled by Jad v1.5.8e. Copyright 2001 Pavel Kouznetsov.
// Jad home page: http://www.geocities.com/kpdus/jad.html
// Decompiler options: braces fieldsfirst space lnc 

package z1;

import a5.a0;
import a5.h0;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.util.Log;
import android.widget.Toast;
import androidx.compose.ui.platform.c0;
import androidx.compose.ui.platform.d1;
import androidx.compose.ui.platform.r0;
import androidx.compose.ui.platform.x1;
import g1.b;
import g1.i;
import h.d;
import h0.l;
import i3.k;
import i3.n;
import i4.e;
import i4.j;
import java.nio.charset.StandardCharsets;
import java.security.SecureRandom;
import java.security.cert.X509Certificate;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicBoolean;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import k.l0;
import k.m;
import k.p0;
import k.q;
import m2.a;
import n3.s0;
import n3.u;
import p.u0;
import q4.p;
import r.b0;
import r.d2;
import r.f;
import r.g;
import r.h1;
import r.j0;
import r.u1;
import r.w0;
import r4.h;

// Referenced classes of package z1:
//            a, b

public final class c
{

    public static final void DefaultPreview(f f1, int i1)
    {
        f1 = f1.n(0x59ce04c3);
        if (i1 == 0 && f1.r())
        {
            f1.c();
        } else
        {
            a2.c.TrendsNotificationTheme(false, a.INSTANCE.getLambda_2D_9$app_release(), f1, 48, 1);
        }
        f1 = f1.O();
        if (f1 == null)
        {
            return;
        } else
        {
            public static final class a extends r4.i
                implements p
            {

                public final int $$changed;

                public volatile Object invoke(Object obj, Object obj1)
                {
                    invoke((f)obj, ((Number)obj1).intValue());
                    return j.a;
                }

                public final void invoke(f f2, int j1)
                {
                    c.DefaultPreview(f2, $$changed | 1);
                }

            public a(int i1)
            {
                $$changed = i1;
                super(2);
            }
            }

            f1.d = new a(i1);
            return;
        }
    }

    public static final void MainContent(f f1, int i1)
    {
        g g1;
label0:
        {
            w0 w0_1;
            j j1;
label1:
            {
                g1 = f1.n(0x66878ced);
                if (i1 == 0 && g1.r())
                {
                    g1.c();
                    break label0;
                }
                g1.d(0xd4dfe628);
                g1.d(0xffc7bcb7);
                Object obj = g1.T();
                r.f.a.a a1 = r.f.a.a;
                f1 = ((f) (obj));
                if (obj == a1)
                {
                    f1 = new b0(j0.d(g1));
                    g1.r0(f1);
                }
                g1.L(false);
                ((b0)f1).getClass();
                g1.L(false);
                g1.d(0xffc7bcb7);
                obj = g1.T();
                f1 = ((f) (obj));
                if (obj == a1)
                {
                    f1 = m2.a.Z0(null);
                    g1.r0(f1);
                }
                g1.L(false);
                w0_1 = (w0)f1;
                j1 = j.a;
                g1.d(0xffc7bdee);
                boolean flag = g1.x(w0_1);
                obj = g1.T();
                if (!flag)
                {
                    f1 = ((f) (obj));
                    if (obj != a1)
                    {
                        break label1;
                    }
                }
                public static final class b extends m4.i
                    implements p
                {

                    public final w0 $result;
                    public Object L$0;
                    public int label;

                    public final k4.d create(Object obj1, k4.d d3)
                    {
                        return new b($result, d3);
                    }

                    public final Object invoke(a0 a0_1, k4.d d3)
                    {
                        return ((b)create(a0_1, d3)).invokeSuspend(j.a);
                    }

                    public volatile Object invoke(Object obj1, Object obj2)
                    {
                        return invoke((a0)obj1, (k4.d)obj2);
                    }

                    public final Object invokeSuspend(Object obj1)
                    {
                        Object obj2 = l4.a.n;
                        int k1 = label;
                        Object obj3;
                        if (k1 != 0)
                        {
                            if (k1 == 1)
                            {
                                obj2 = (w0)L$0;
                                m2.a.t1(obj1);
                                obj3 = obj1;
                            } else
                            {
                                throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                            }
                        } else
                        {
                            m2.a.t1(obj1);
                            obj1 = $result;
                            L$0 = obj1;
                            label = 1;
                            obj3 = c.crawling(this);
                            if (obj3 == obj2)
                            {
                                return obj2;
                            }
                            obj2 = obj1;
                        }
                        ((w0) (obj2)).setValue(obj3);
                        return j.a;
                    }

            public b(w0 w0_1, k4.d d3)
            {
                $result = w0_1;
                super(2, d3);
            }
                }

                f1 = new b(w0_1, null);
                g1.r0(f1);
            }
            g1.L(false);
            j0.c(j1, (p)f1, g1);
            if (w0_1.getValue() != null)
            {
                g1.d(0x66878ddf);
                f1 = ((f) (w0_1.getValue()));
                r4.h.b(f1);
                Screen((Map)f1, g1, 8);
            } else
            {
                g1.d(0x66878e0b);
                p.l0.a(l0.a(), 0L, 0.0F, g1, 6, 6);
            }
            g1.L(false);
        }
        f1 = g1.O();
        if (f1 == null)
        {
            return;
        } else
        {
            public static final class c extends r4.i
                implements p
            {

                public final int $$changed;

                public volatile Object invoke(Object obj1, Object obj2)
                {
                    invoke((f)obj1, ((Number)obj2).intValue());
                    return j.a;
                }

                public final void invoke(f f2, int k1)
                {
                    c.MainContent(f2, $$changed | 1);
                }

            public c(int i1)
            {
                $$changed = i1;
                super(2);
            }
            }

            f1.d = new c(i1);
            return;
        }
    }

    public static final void Screen(Map map, f f1, int i1)
    {
label0:
        {
            Object obj;
            g g1;
            r.f.a.a a1;
            w0 w0_1;
            w0 w0_2;
label1:
            {
                r4.h.d(map, "result");
                g1 = f1.n(0x63a82e0d);
                g1.d(0xffc7bcb7);
                obj = g1.T();
                a1 = r.f.a.a;
                f1 = ((f) (obj));
                if (obj == a1)
                {
                    f1 = m2.a.Z0(Boolean.FALSE);
                    g1.r0(f1);
                }
                g1.L(false);
                w0_1 = (w0)f1;
                g1.d(0xffc7bcb7);
                obj = g1.T();
                f1 = ((f) (obj));
                if (obj == a1)
                {
                    f1 = m2.a.Z0("");
                    g1.r0(f1);
                }
                g1.L(false);
                w0_2 = (w0)f1;
                f1 = (Context)g1.j(c0.b);
                Object obj1 = c0.a.a.f;
                obj = l0.b();
                float f2 = 50;
                float f4 = 0;
                Object obj3 = d1.a;
                obj3 = new q(f4, f2, f4, f2);
                obj = ((m)obj).H(((c0.f) (obj3)));
                g1.d(0xbda87efd);
                obj3 = k.a.a;
                obj1 = k.h.a(((c0.b.a) (obj1)), g1);
                g1.d(0x52057532);
                obj3 = (b)g1.j(r0.e);
                i j1 = (i)g1.j(r0.j);
                x1 x1_1 = (x1)g1.j(r0.n);
                r0.a.d.getClass();
                r0.n.a a3 = r0.a.a.b;
                obj = m2.a.U0(((c0.f) (obj)));
                if (!(g1.a instanceof r.c))
                {
                    break label0;
                }
                g1.q();
                if (g1.I)
                {
                    g1.e(a3);
                } else
                {
                    g1.m();
                }
                g1.w = false;
                m2.a.m1(g1, obj1, r0.a.a.e);
                m2.a.m1(g1, obj3, r0.a.a.d);
                m2.a.m1(g1, j1, r0.a.a.f);
                m2.a.m1(g1, x1_1, r0.a.a.g);
                g1.g();
                ((y.a) (obj)).invoke(new u1(g1), g1, Integer.valueOf(0));
                g1.d(0x7ab4aae9);
                g1.d(0x107e0279);
                long l2 = m2.a.x0(25);
                long l1 = l.c;
                u0.b("Trends Notification", null, l1, l2, null, null, null, 0L, null, null, 0L, 0, false, 0, null, null, g1, 3462, 0, 65522);
                p0.a(l0.c(30), g1, 6);
                boolean flag;
                if (Screen$lambda_2D_6(w0_2).length() == 0)
                {
                    flag = true;
                } else
                {
                    flag = false;
                }
                if (flag)
                {
                    g1.d(0x99cfb6ee);
                    u0.b("Please click the button below to see the news headlines.", null, l1, m2.a.x0(16), null, null, null, 0L, null, null, 0L, 0, false, 0, null, null, g1, 3462, 0, 65522);
                    g1.L(false);
                } else
                {
                    g1.d(0x99cfb7b1);
                    p0.a(l0.c(20), g1, 6);
                    obj = new StringBuilder();
                    ((StringBuilder) (obj)).append("Top: ");
                    ((StringBuilder) (obj)).append(map.get("top"));
                    ((StringBuilder) (obj)).append("\n\n");
                    obj = ((StringBuilder) (obj)).toString();
                    long l3 = m2.a.x0(25);
                    public static final class d extends r4.i
                        implements q4.a
                    {

                        public final Context $context;
                        public final Map $result;

                        public volatile Object invoke()
                        {
                            invoke();
                            return j.a;
                        }

                        public final void invoke()
                        {
                            String s = r4.h.g($result.get("top_link"), "http://www.itworld.co.kr");
                            $context.startActivity(new Intent("android.intent.action.VIEW", Uri.parse(s)));
                        }

            public d(Map map, Context context)
            {
                $result = map;
                $context = context;
                super(0);
            }
                    }

                    u0.b(((String) (obj)), h.d.c(new d(map, f1)), l1, l3, null, null, null, 0L, null, null, 0L, 0, false, 0, null, null, g1, 3456, 0, 65520);
                    float f3 = 10;
                    p0.a(l0.c(f3), g1, 6);
                    obj = new StringBuilder();
                    ((StringBuilder) (obj)).append("AI: ");
                    ((StringBuilder) (obj)).append(map.get("ai"));
                    ((StringBuilder) (obj)).append("\n\n");
                    obj = ((StringBuilder) (obj)).toString();
                    l3 = m2.a.x0(25);
                    public static final class e extends r4.i
                        implements q4.a
                    {

                        public final Context $context;
                        public final Map $result;

                        public volatile Object invoke()
                        {
                            invoke();
                            return j.a;
                        }

                        public final void invoke()
                        {
                            String s = r4.h.g($result.get("ai_link"), "http://www.itworld.co.kr");
                            $context.startActivity(new Intent("android.intent.action.VIEW", Uri.parse(s)));
                        }

            public e(Map map, Context context)
            {
                $result = map;
                $context = context;
                super(0);
            }
                    }

                    u0.b(((String) (obj)), h.d.c(new e(map, f1)), l1, l3, null, null, null, 0L, null, null, 0L, 0, false, 0, null, null, g1, 3456, 0, 65520);
                    p0.a(l0.c(f3), g1, 6);
                    obj = new StringBuilder();
                    ((StringBuilder) (obj)).append("Security: ");
                    ((StringBuilder) (obj)).append(map.get("security"));
                    ((StringBuilder) (obj)).append("\n\n");
                    obj = ((StringBuilder) (obj)).toString();
                    l3 = m2.a.x0(25);
                    public static final class f extends r4.i
                        implements q4.a
                    {

                        public final Context $context;
                        public final Map $result;

                        public volatile Object invoke()
                        {
                            invoke();
                            return j.a;
                        }

                        public final void invoke()
                        {
                            String s = r4.h.g($result.get("security_link"), "http://www.itworld.co.kr");
                            $context.startActivity(new Intent("android.intent.action.VIEW", Uri.parse(s)));
                        }

            public f(Map map, Context context)
            {
                $result = map;
                $context = context;
                super(0);
            }
                    }

                    u0.b(((String) (obj)), h.d.c(new f(map, f1)), l1, l3, null, null, null, 0L, null, null, 0L, 0, false, 0, null, null, g1, 3456, 0, 65520);
                    p0.a(l0.c(f3), g1, 6);
                    obj = new StringBuilder();
                    ((StringBuilder) (obj)).append("key: ");
                    ((StringBuilder) (obj)).append(map.get("key"));
                    ((StringBuilder) (obj)).append("\n\n");
                    u0.b(((StringBuilder) (obj)).toString(), null, l1, m2.a.x0(25), null, null, null, 0L, null, null, 0L, 0, false, 0, null, null, g1, 3456, 0, 65522);
                    g1.L(false);
                }
                obj = f1;
                p0.a(l0.c(500), g1, 6);
                g1.d(0xffc7bdee);
                boolean flag1 = g1.x(w0_1);
                obj1 = g1.T();
                if (!flag1)
                {
                    f1 = ((f) (obj1));
                    if (obj1 != a1)
                    {
                        break label1;
                    }
                }
                public static final class g extends r4.i
                    implements q4.a
                {

                    public final w0 $showDialog$delegate;

                    public volatile Object invoke()
                    {
                        invoke();
                        return j.a;
                    }

                    public final void invoke()
                    {
                        c.Screen$lambda_2D_4($showDialog$delegate, true);
                    }

            public g(w0 w0_1)
            {
                $showDialog$delegate = w0_1;
                super(0);
            }
                }

                f1 = new g(w0_1);
                g1.r0(f1);
            }
label2:
            {
                z1.a a2;
label3:
                {
                    g1.L(false);
                    f1 = (q4.a)f1;
                    boolean flag2 = encrypt_data_check("flag");
                    a2 = a.INSTANCE;
                    m2.a.e(f1, null, flag2, null, null, null, null, null, a2.getLambda_2D_4$app_release(), g1, 0x30000000, 506);
                    g1.L(false);
                    g1.L(false);
                    g1.L(true);
                    g1.L(false);
                    g1.L(false);
                    if (!Screen$lambda_2D_3(w0_1))
                    {
                        break label2;
                    }
                    g1.d(0xffc7bdee);
                    flag2 = g1.x(w0_1);
                    Object obj2 = g1.T();
                    if (!flag2)
                    {
                        f1 = ((f) (obj2));
                        if (obj2 != a1)
                        {
                            break label3;
                        }
                    }
                    public static final class h extends r4.i
                        implements q4.a
                    {

                        public final w0 $showDialog$delegate;

                        public volatile Object invoke()
                        {
                            invoke();
                            return j.a;
                        }

                        public final void invoke()
                        {
                            c.Screen$lambda_2D_4($showDialog$delegate, false);
                        }

            public h(w0 w0_1)
            {
                $showDialog$delegate = w0_1;
                super(0);
            }
                    }

                    f1 = new h(w0_1);
                    g1.r0(f1);
                }
                g1.L(false);
                public static final class i extends r4.i
                    implements p
                {

                    public final Context $context;
                    public final w0 $showDialog$delegate;
                    public final w0 $textViewText$delegate;

                    public volatile Object invoke(Object obj4, Object obj5)
                    {
                        invoke((f)obj4, ((Number)obj5).intValue());
                        return j.a;
                    }

                    public final void invoke(f f5, int k1)
                    {
                        if ((k1 & 0xb ^ 2) == 0 && f5.r())
                        {
                            f5.c();
                            return;
                        } else
                        {
                            public static final class i.a extends r4.i
                                implements q4.a
                            {

                                public final Context $context;
                                public final w0 $showDialog$delegate;
                                public final w0 $textViewText$delegate;

                                public volatile Object invoke()
                                {
                                    invoke();
                                    return j.a;
                                }

                                public final void invoke()
                                {
                                    Toast.makeText($context, "Find Success Trends", 0).show();
                                    c.Screen$lambda_2D_7($textViewText$delegate, "Headlines");
                                    c.Screen$lambda_2D_4($showDialog$delegate, false);
                                }

            public i.a(Context context, w0 w0_1, w0 w0_2)
            {
                $context = context;
                $textViewText$delegate = w0_1;
                $showDialog$delegate = w0_2;
                super(0);
            }
                            }

                            m2.a.q(new a($context, $textViewText$delegate, $showDialog$delegate), null, false, null, null, null, null, null, a.INSTANCE.getLambda_2D_5$app_release(), f5, 0x30000000, 510);
                            return;
                        }
                    }

            public i(Context context, w0 w0_1, w0 w0_2)
            {
                $context = context;
                $textViewText$delegate = w0_1;
                $showDialog$delegate = w0_2;
                super(2);
            }
                }

                public static final class j extends r4.i
                    implements p
                {

                    public final Context $context;
                    public final w0 $showDialog$delegate;

                    public volatile Object invoke(Object obj4, Object obj5)
                    {
                        invoke((f)obj4, ((Number)obj5).intValue());
                        return j.a;
                    }

                    public final void invoke(f f5, int k1)
                    {
                        if ((k1 & 0xb ^ 2) == 0 && f5.r())
                        {
                            f5.c();
                            return;
                        } else
                        {
                            public static final class j.a extends r4.i
                                implements q4.a
                            {

                                public final Context $context;
                                public final w0 $showDialog$delegate;

                                public volatile Object invoke()
                                {
                                    invoke();
                                    return j.a;
                                }

                                public final void invoke()
                                {
                                    Toast.makeText($context, "cancel", 0).show();
                                    c.Screen$lambda_2D_4($showDialog$delegate, false);
                                }

            public j.a(Context context, w0 w0_1)
            {
                $context = context;
                $showDialog$delegate = w0_1;
                super(0);
            }
                            }

                            m2.a.q(new a($context, $showDialog$delegate), null, false, null, null, null, null, null, a.INSTANCE.getLambda_2D_6$app_release(), f5, 0x30000000, 510);
                            return;
                        }
                    }

            public j(Context context, w0 w0_1)
            {
                $context = context;
                $showDialog$delegate = w0_1;
                super(2);
            }
                }

                p.i.a((q4.a)f1, m2.a.S(g1, 0xcf2173ed, new i(((Context) (obj)), w0_2, w0_1)), null, m2.a.S(g1, 0xcf217069, new j(((Context) (obj)), w0_1)), a2.getLambda_2D_7$app_release(), a2.getLambda_2D_8$app_release(), null, 0L, 0L, null, g1, 0x36c30, 964);
            }
            f1 = g1.O();
            if (f1 == null)
            {
                return;
            } else
            {
                public static final class k extends r4.i
                    implements p
                {

                    public final int $$changed;
                    public final Map $result;

                    public volatile Object invoke(Object obj4, Object obj5)
                    {
                        invoke((f)obj4, ((Number)obj5).intValue());
                        return j.a;
                    }

                    public final void invoke(f f5, int k1)
                    {
                        c.Screen($result, f5, $$changed | 1);
                    }

            public k(Map map, int i1)
            {
                $result = map;
                $$changed = i1;
                super(2);
            }
                }

                f1.d = new k(map, i1);
                return;
            }
        }
        a5.j.H();
        throw null;
    }

    private static final boolean Screen$lambda_2D_3(w0 w0_1)
    {
        return ((Boolean)w0_1.getValue()).booleanValue();
    }

    private static final void Screen$lambda_2D_4(w0 w0_1, boolean flag)
    {
        w0_1.setValue(Boolean.valueOf(flag));
    }

    private static final String Screen$lambda_2D_6(w0 w0_1)
    {
        return (String)w0_1.getValue();
    }

    private static final void Screen$lambda_2D_7(w0 w0_1, String s)
    {
        w0_1.setValue(s);
    }

    public static boolean a(String s, SSLSession sslsession)
    {
        return disableSSLCertificateCheck$lambda_2D_13(s, sslsession);
    }

    public static final Object crawling(k4.d d3)
    {
        public static final class l extends m4.i
            implements p
        {

            public Object L$0;
            public Object L$1;
            public Object L$2;
            public Object L$3;
            public Object L$4;
            public Object L$5;
            public int label;

            public final k4.d create(Object obj, k4.d d4)
            {
                return new l(d4);
            }

            public final Object invoke(a0 a0_1, k4.d d4)
            {
                return ((l)create(a0_1, d4)).invokeSuspend(j.a);
            }

            public volatile Object invoke(Object obj, Object obj1)
            {
                return invoke((a0)obj, (k4.d)obj1);
            }

            public final Object invokeSuspend(Object obj)
            {
                Object obj6;
                int i1;
                obj6 = l4.a.n;
                i1 = label;
                if (i1 == 0) goto _L2; else goto _L1
_L1:
                Object obj1;
                Object obj2;
                Object obj3;
                Object obj4;
                Object obj5;
                Object obj7;
                if (i1 == 1)
                {
                    obj1 = (String)L$5;
                    obj3 = (String)L$4;
                    obj2 = (String)L$3;
                    obj5 = (String)L$2;
                    obj4 = (String)L$1;
                    obj6 = (String)L$0;
                    try
                    {
                        m2.a.t1(obj);
                    }
                    // Misplaced declaration of an exception variable
                    catch (Object obj)
                    {
                        Log.e("crawling", obj.toString());
                        return j4.p.n;
                    }
                } else
                {
                    throw new IllegalStateException("call to 'resume' before 'invoke' with coroutine");
                }
                  goto _L3
_L2:
                m2.a.t1(obj);
                c.disableSSLCertificateCheck();
                obj1 = i5.d.a("http://www.itworld.co.kr/main/").b();
                obj3 = i5.d.a("http://www.itworld.co.kr/t/69500/AI%E3%86%8DML").b();
                obj5 = i5.d.a("http://www.itworld.co.kr/t/36/%EB%B3%B4%EC%95%88").b();
                obj = ((l5.i) (obj1)).L("h5[class='card-title crop-text mt-1 fw-bold'] > a").a();
                if (obj == null)
                {
                    obj = null;
                    break MISSING_BLOCK_LABEL_151;
                }
                obj = ((l5.i) (obj)).N();
                obj1 = ((l5.i) (obj1)).L("h5[class='card-title crop-text mt-1 fw-bold'] > a").a();
                if (obj1 == null)
                {
                    obj1 = null;
                    break MISSING_BLOCK_LABEL_177;
                }
                obj1 = ((l5.m) (obj1)).c("href");
                obj2 = ((l5.i) (obj3)).L("h5[class='card-title'] > a").a();
                if (obj2 == null)
                {
                    obj2 = null;
                    break MISSING_BLOCK_LABEL_202;
                }
                obj2 = ((l5.i) (obj2)).N();
                obj3 = ((l5.i) (obj3)).L("h5[class='card-title'] > a").a();
                if (obj3 == null)
                {
                    obj3 = null;
                    break MISSING_BLOCK_LABEL_234;
                }
                obj3 = ((l5.m) (obj3)).c("href");
                obj4 = ((l5.i) (obj5)).L("h5[class='card-title'] > a").a();
                if (obj4 == null)
                {
                    obj4 = null;
                    break MISSING_BLOCK_LABEL_264;
                }
                obj4 = ((l5.i) (obj4)).N();
                obj5 = ((l5.i) (obj5)).L("h5[class='card-title'] > a").a();
                if (obj5 == null)
                {
                    obj5 = null;
                    break MISSING_BLOCK_LABEL_296;
                }
                obj5 = ((l5.m) (obj5)).c("href");
                obj7 = i3.g.a().b().a("trends").a("key");
                L$0 = obj;
                L$1 = obj1;
                L$2 = obj2;
                L$3 = obj3;
                L$4 = obj4;
                L$5 = obj5;
                label = 1;
                obj7 = c.getKeyFromDatabase(((i3.d) (obj7)), this);
                if (obj7 == obj6)
                {
                    return obj6;
                }
                obj6 = obj1;
                Object obj8 = obj3;
                Object obj9 = obj2;
                obj3 = obj4;
                obj1 = obj5;
                obj2 = obj8;
                obj5 = obj9;
                obj4 = obj6;
                obj6 = obj;
                obj = obj7;
                  goto _L4
_L3:
                obj7 = (String)obj;
                c.encrypt("flag", ((String) (obj7)));
                obj = obj6;
                if (obj6 == null)
                {
                    obj = "";
                }
                obj6 = new e("top", obj);
                obj = obj5;
                if (obj5 == null)
                {
                    obj = "";
                }
                obj5 = new e("ai", obj);
                obj = obj3;
                if (obj3 == null)
                {
                    obj = "";
                }
                obj3 = new e("security", obj);
                obj = obj4;
                if (obj4 == null)
                {
                    obj = "";
                }
                obj4 = new e("top_link", obj);
                obj = obj2;
                if (obj2 == null)
                {
                    obj = "";
                }
                obj2 = new e("ai_link", obj);
                obj = obj1;
                if (obj1 == null)
                {
                    obj = "";
                }
                obj = j4.j.W1(new e[] {
                    obj6, obj5, obj3, obj4, obj2, new e("security_link", obj), new e("key", obj7)
                });
                return obj;
_L4:
                if (true) goto _L3; else goto _L5
_L5:
            }

            public l(k4.d d3)
            {
                super(2, d3);
            }
        }

        return m2.a.E1(h0.b, new l(null), d3);
    }

    public static final String customOperation(String s)
    {
        r4.h.d(s, "text");
        ArrayList arraylist = new ArrayList(s.length());
        int j1 = 0;
        for (int i1 = 0; j1 < s.length(); i1++)
        {
            char c1 = s.charAt(j1);
            j1++;
            arraylist.add(Character.valueOf((char)((c1 + i1) % 256)));
        }

        return j4.m.a2(arraylist, "", null, null, null, 62);
    }

    public static final void disableSSLCertificateCheck()
    {
        public static final class m
            implements X509TrustManager
        {

            public void checkClientTrusted(X509Certificate ax509certificate[], String s)
            {
                r4.h.d(ax509certificate, "chain");
                r4.h.d(s, "authType");
            }

            public void checkServerTrusted(X509Certificate ax509certificate[], String s)
            {
                r4.h.d(ax509certificate, "chain");
                r4.h.d(s, "authType");
            }

            public X509Certificate[] getAcceptedIssuers()
            {
                return new X509Certificate[0];
            }

            public m()
            {
            }
        }

        m m1 = new m();
        SSLContext sslcontext = SSLContext.getInstance("TLS");
        SecureRandom securerandom = new SecureRandom();
        sslcontext.init(null, new TrustManager[] {
            m1
        }, securerandom);
        HttpsURLConnection.setDefaultSSLSocketFactory(sslcontext.getSocketFactory());
        HttpsURLConnection.setDefaultHostnameVerifier(new z1.b());
    }

    private static final boolean disableSSLCertificateCheck$lambda_2D_13(String s, SSLSession sslsession)
    {
        return true;
    }

    public static final String encrypt(String s, String s1)
    {
        r4.h.d(s, "text");
        r4.h.d(s1, "key");
        s = customOperation(xorOperation(s, s1));
        s1 = StandardCharsets.UTF_8;
        r4.h.c(s1, "UTF_8");
        s1 = s.getBytes(s1);
        r4.h.c(s1, "this as java.lang.String).getBytes(charset)");
        public static final class n extends r4.i
            implements q4.l
        {

            public static final n INSTANCE = new n();

            public final CharSequence invoke(byte byte1)
            {
                String s2 = String.format("%02x", Arrays.copyOf(new Object[] {
                    Byte.valueOf(byte1)
                }, 1));
                r4.h.c(s2, "format(format, *args)");
                return s2;
            }

            public volatile Object invoke(Object obj)
            {
                return invoke(((Number)obj).byteValue());
            }


            public n()
            {
                super(1);
            }
        }

        n n1 = n.INSTANCE;
        StringBuilder stringbuilder = new StringBuilder();
        stringbuilder.append("");
        int k1 = s1.length;
        int j1 = 0;
        int i1 = 0;
        while (j1 < k1) 
        {
            byte byte0 = s1[j1];
            j1++;
            i1++;
            if (i1 > 1)
            {
                stringbuilder.append("");
            }
            if (n1 != null)
            {
                s = (CharSequence)n1.invoke(Byte.valueOf(byte0));
            } else
            {
                s = String.valueOf(byte0);
            }
            stringbuilder.append(s);
        }
        stringbuilder.append("");
        s = stringbuilder.toString();
        r4.h.c(s, "joinTo(StringBuilder(), \u2026ed, transform).toString()");
        return s;
    }

    public static final boolean encrypt_data_check(String s)
    {
        r4.h.d(s, "encrypt_data");
        return s == "0f010a0c0c121e1166656763236c68636c69676a6e6a20247524797679717675752b7b7b787b7b7c327d7fc288c2863e";
    }

    public static final Object getKeyFromDatabase(i3.d d3, k4.d d4)
    {
        a5.i i1;
        n3.p0 p0_1;
        s0 s0_1;
        boolean flag;
        d4 = a5.j.G(d4);
        flag = true;
        i1 = new a5.i(1, d4);
        i1.m();
        public static final class o
            implements i3.p
        {

            public final a5.h $continuation;

            public void onCancelled(i3.b b1)
            {
                r4.h.d(b1, "error");
                $continuation.resumeWith("");
            }

            public void onDataChange(i3.a a1)
            {
                r4.h.d(a1, "snapshot");
                a1 = (String)r3.a.b(a1.a.n.getValue(), java/lang/String);
                if (a1 != null)
                {
                    $continuation.resumeWith(a1);
                    return;
                } else
                {
                    $continuation.resumeWith("");
                    return;
                }
            }

            public o(a5.h h2)
            {
                $continuation = h2;
                super();
            }
        }

        d4 = new o(i1);
        p0_1 = new n3.p0(((n) (d3)).a, new k(d3, d4), new s3.k(((n) (d3)).b, ((n) (d3)).c));
        s0_1 = s0.b;
        HashMap hashmap = s0_1.a;
        hashmap;
        JVM INSTR monitorenter ;
        List list = (List)s0_1.a.get(p0_1);
        d4 = list;
        if (list != null)
        {
            break MISSING_BLOCK_LABEL_123;
        }
        d4 = new ArrayList();
        s0_1.a.put(p0_1, d4);
        n3.p0 p0_2;
        d4.add(p0_1);
        if (p0_1.f.b())
        {
            break MISSING_BLOCK_LABEL_213;
        }
        p0_2 = p0_1.a(s3.k.a(p0_1.f.a));
        list = (List)s0_1.a.get(p0_2);
        d4 = list;
        if (list != null)
        {
            break MISSING_BLOCK_LABEL_201;
        }
        d4 = new ArrayList();
        s0_1.a.put(p0_2, d4);
        d4.add(p0_1);
        p0_1.c = true;
        q3.i.c(((n3.i) (p0_1)).a.get() ^ true);
        if (((n3.i) (p0_1)).b != null)
        {
            flag = false;
        }
        q3.i.c(flag);
        p0_1.b = s0_1;
        hashmap;
        JVM INSTR monitorexit ;
        ((n) (d3)).a.h(new i3.m(d3, p0_1));
        return i1.k();
_L2:
        hashmap;
        JVM INSTR monitorexit ;
        throw d3;
        d3;
        if (true) goto _L2; else goto _L1
_L1:
    }

    public static final String xorOperation(String s, String s1)
    {
        int j2;
label0:
        {
            Object obj;
            boolean flag1;
label1:
            {
                r4.h.d(s, "text");
                r4.h.d(s1, "key");
                j2 = s.length() / s1.length();
                flag1 = false;
                boolean flag2 = true;
                boolean flag;
                if (j2 >= 0)
                {
                    flag = true;
                } else
                {
                    flag = false;
                }
                if (!flag)
                {
                    break label0;
                }
                if (j2 != 0)
                {
                    if (j2 != 1)
                    {
                        int i1 = s1.length();
                        if (i1 != 0)
                        {
                            if (i1 != 1)
                            {
                                obj = new StringBuilder(s1.length() * j2);
                                if (1 <= j2)
                                {
                                    int j1 = ((flag2) ? 1 : 0);
                                    do
                                    {
                                        ((StringBuilder) (obj)).append(s1);
                                        if (j1 == j2)
                                        {
                                            break;
                                        }
                                        j1++;
                                    } while (true);
                                }
                                obj = ((StringBuilder) (obj)).toString();
                                r4.h.c(obj, "{\n                    va\u2026tring()\n                }");
                            } else
                            {
                                char c1 = s1.charAt(0);
                                obj = new char[j2];
                                for (int k1 = 0; k1 < j2; k1++)
                                {
                                    obj[k1] = c1;
                                }

                                obj = new String(((char []) (obj)));
                            }
                            break label1;
                        }
                    } else
                    {
                        obj = s1.toString();
                        break label1;
                    }
                }
                obj = "";
            }
            s1 = s1.substring(0, s.length() % s1.length());
            r4.h.c(s1, "this as java.lang.String\u2026ing(startIndex, endIndex)");
            s1 = r4.h.g(s1, ((String) (obj)));
            int i2 = Math.min(s.length(), s1.length());
            obj = new ArrayList(i2);
            for (int l1 = ((flag1) ? 1 : 0); l1 < i2; l1++)
            {
                char c2 = s.charAt(l1);
                ((ArrayList) (obj)).add(Integer.valueOf(s1.charAt(l1) ^ c2));
            }

            public static final class p extends r4.i
                implements q4.l
            {

                public static final p INSTANCE = new p();

                public final CharSequence invoke(int k2)
                {
                    return String.valueOf((char)k2);
                }

                public volatile Object invoke(Object obj1)
                {
                    return invoke(((Number)obj1).intValue());
                }


            public p()
            {
                super(1);
            }
            }

            return j4.m.a2(((Iterable) (obj)), "", null, null, p.INSTANCE, 30);
        }
        s = new StringBuilder();
        s.append("Count 'n' must be non-negative, but was ");
        s.append(j2);
        s.append('.');
        throw new IllegalArgumentException(s.toString().toString());
    }


}
