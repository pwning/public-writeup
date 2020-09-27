#![allow(dead_code)]

extern crate ramp;
use indicatif::{ProgressBar, ProgressStyle};
use ramp::Int;
use std::str::FromStr;

#[derive(Clone)]
struct Constants {
    p: Int,
    r: Int,
    k: Int,
    n: Int,
    e: Int,
    s: Int,
    b: Int,
}

fn constants() -> Constants {
    let p = Int::from_str("6722156186149423473586056936189163112345526308304739592548269432948561498704906497631759731744824085311511299618196491816929603296108414569727189748975204102209646335725406551943711581704258725226874414399572244863268492324353927787818836752142254189928999592648333789131233670456465647924867060170327150559233").unwrap();
    let r = Int::from_str("1948865039294009691576181380771672389220382961994854292305692557649261763833149884145614983319207887860531232498119502026176334583810204964826290882842308810728384018930976243008464049012096415817825074466275128141940107121005470692979995184344972514864128534992403176506223940852066206954491827309484962494271").unwrap();
    let k = Int::from_str("3438332358968490881344155919145296251372757080629150991804744990816498140172070879978289432582589956941900786739276293096894841598246547366222142431811946062855877251326280341791697983338980798885639158045676757585753720032188339269806684469725099875846539885354821848894557007698661810185229270603897638348409").unwrap();
    let n = Int::from_str(
        "46118657867174982362767620809194528394371823889882751901998575652536398788270410454086398546385305600",
    )
    .unwrap();
    let e = Int::one() << 64;
    let s = Int::from_str("5602276430032875007249509644314357293319755912603737631044802989314683039473469151600643674831915676677562504743413434940280819915470852112137937963496770923674944514657123370759858913638782767380945111493317828235741160391407042689991007589804877919105123960837253705596164618906554015382923343311865102111160").unwrap();
    let b = Int::one() << (8 * (42 - 6));
    Constants {
        p,
        r,
        k,
        n,
        e,
        s,
        b,
    }
}

fn test(c: &Constants, i: u64) -> (bool, Int) {
    let i: Int = i.into();
    let v = (&c.r * (c.k.pow_mod(&i, &c.p))) % &c.p;
    if c.n < v && v < &c.n + &c.b {
        println!("At {}, found: {}", i, v);
        std::fs::write(format!("{}", i), format!("{}", v)).unwrap();
        (true, v)
    } else {
        (false, v)
    }
}

fn main() {
    let constants = constants();

    // sanity check tests
    assert_eq!(
        test(&constants, 0).1.pow_mod(&constants.e, &constants.p),
        constants.s
    );
    assert_eq!(
        test(&constants, 4).1.pow_mod(&constants.e, &constants.p),
        constants.s
    );
    assert_ne!(test(&constants, 0).1, test(&constants, 4).1);

    let range_min = 0;
    let range_max = 1 << 30;
    let pool_size = 14;
    let mut threads = vec![];
    let spl = ((range_max - range_min) + pool_size - 1) / pool_size;
    let pb_main = std::sync::Arc::new(ProgressBar::new(range_max));
    pb_main.set_style(ProgressStyle::default_bar().template(
        "[{elapsed_precise} elapsed] [{eta_precise} eta] [{per_sec} it/s] {bar:50.cyan/blue} {pos:>7}/{len:7}",
    ));
    let pb_refresh_rate = 10000;
    for i in 0..pool_size {
        let constants = constants.clone();
        let pb_main = pb_main.clone();
        threads.push(std::thread::spawn(move || {
            for m in range_min + i * spl..range_min + (i + 1) * spl {
                if m % pb_refresh_rate == 0 {
                    pb_main.inc(pb_refresh_rate);
                }
                test(&constants, m);
            }
        }));
    }
    for thr in threads {
        thr.join().unwrap();
    }
    pb_main.finish();
}
