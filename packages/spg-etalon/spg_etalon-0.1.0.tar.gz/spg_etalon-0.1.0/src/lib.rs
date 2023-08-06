use pyo3::prelude::*;
use num_complex::Complex;
use rayon::prelude::*;
// use std::thread;
// use std::sync::mpsc;
extern crate num_cpus;

pub const PI: f64 = 3.14159265358979323846264338327950288f64; // 3.14159274f64
pub const J: Complex<f64> = Complex::<f64>::new(0.0, 1.0);

#[pyclass]
pub struct EtalonProp { /// Etalon basic parameters
  #[pyo3(get)]
  pub wvl0: f64,
  #[pyo3(get)]
  pub fnum: f64,
  #[pyo3(get)]
  pub no: f64,
  #[pyo3(get)]
  pub ne: f64,
  #[pyo3(get)]
  pub h: f64,
  #[pyo3(get)]
  pub r: f64,
  #[pyo3(get)]
  pub a: f64,
  #[pyo3(get)]
  pub wvl: f64,
  #[pyo3(get)]
  pub m: f64,
  #[pyo3(get)]
  pub d_h: f64,
  #[pyo3(get)]
  pub tau: f64,
  #[pyo3(get)]
  pub fin: f64,
  #[pyo3(get)]
  pub rp: f64,
  #[pyo3(get)]
  pub f: f64,
  #[pyo3(get, set)]
  pub tol: f64,
  #[pyo3(get)]
  pub intr: Vec<f64>,
  #[pyo3(get)]
  pub intt: Vec<f64>,
  #[pyo3(get, set)]
  pub theta3: f64,
}

#[pymethods]
impl EtalonProp {
    #[new]
    fn new() -> EtalonProp {
        let wvl0: f64  = 617.3e-9;
        let fnum: f64  = 63.5;
        let no: f64  = 2.29;
        let ne: f64  = no.clone();
        let mut h: f64  = 250e-6;
        let r: f64  = 0.92;
        let a: f64  = 0.;
        let wvl: f64 = wvl0+wvl0/(16.0 * no.powf(2.0) * fnum.powf(2.0) ) ;
        let m: f64 = (2.0*no*h/wvl0).round();
        let d_h: f64 = (m * wvl - 2.0 * no * h)/(2.0 * no);
        h = h + d_h;
        let tau: f64 = (1.0 - a / (1.0 - r)).powf(2.0);
        let fin: f64 = 4.0 * r / (1.0 - r).powf(2.0);   
        let tol: f64  = 1e-10;
        let rp: f64 = 17.5e-3 / 2.0 ;
        let f: f64 = 2.0 * rp * fnum ;
        let intr = vec![0.0, rp, 50.0];
        let intt = vec![0.0, 2.0 * PI, 50.0];
        let theta3: f64 = 0.0;
        EtalonProp { wvl0, fnum , no, ne, h, r, a, wvl, m, d_h, tau, fin, rp, f, tol, intr, intt, theta3} 
    }
    #[setter]
    fn set_wvl0(&mut self, value: f64) -> PyResult<()> {
        self.wvl0 = value;
        self.update();
        Ok(())
    }
    #[setter]
    fn set_fnum(&mut self, value: f64) -> PyResult<()> {
        self.fnum = value;
        self.update();
        Ok(())
    }
    #[setter]
    fn set_no(&mut self, value: f64) -> PyResult<()> {
        self.no = value;
        self.update();
        Ok(())
    }
    #[setter]
    fn set_ne(&mut self, value: f64) -> PyResult<()> {
        self.ne = value;
        self.update();
        Ok(())
    }
    #[setter]
    fn set_h(&mut self, value: f64) -> PyResult<()> {
        self.h = value;
        self.update();
        Ok(())
    }
    #[setter]
    fn set_r(&mut self, value: f64) -> PyResult<()> {
        self.r = value;
        self.update();
        Ok(())
    }
    #[setter]
    fn set_a(&mut self, value: f64) -> PyResult<()> {
        self.a = value;
        self.update();
        Ok(())
    }
    #[setter]
    fn set_rp(&mut self, value: f64) -> PyResult<()> {
        self.rp = value;
        self.update();
        self.intr[1] = self.rp;
        Ok(())
    }
    #[setter]
    fn set_f(&mut self, value: f64) -> PyResult<()> {
        self.f = value;
        Ok(())
    }
    #[setter]
    fn set_intr(&mut self, value: Vec<f64>) -> PyResult<()> {
        let nl: usize = value.len(); 
        if nl == 3 {
            self.intr = value;
            println!("Changes integration indices in intr to {:?}",self.intr );
        } else {println!("Error setting intr (need to be three elements list) {:?}",value ); };
        Ok(())
    }
    #[setter]
    fn set_intt(&mut self, value: Vec<f64>) -> PyResult<()> {
        let nl: usize = value.len(); 
        if nl == 3 {
            self.intt = value;
            println!("Changes integration indices in intt to {:?}",self.intt );
        } else {println!("Error setting intt (need to be three elements list) {:?}",value ); };
        Ok(())
    }
    fn update(&mut self){
        self.wvl = self.wvl0+self.wvl0/(16.0 * self.no.powf(2.0) * self.fnum.powf(2.0) ) ;
        self.m = (2.0*self.no*self.h/self.wvl0).round();
        self.d_h = (self.m * self.wvl - 2.0 * self.no * self.h)/(2.0 * self.no);
        self.tau = (1.0 - self.a / (1.0 - self.r)).powf(2.0);
        self.fin = 4.0 * self.r / (1.0 - self.r).powf(2.0);
        self.f = 2.0 * self.rp * self.fnum;
    }
    pub fn show(&self) {
        println!("-----------------Etalon main parameters------------------");
        println!("(wvl0) Central wavelength [m]:            {:+e}", self.wvl0);
        println!("(fnum) f number:                          {}", self.fnum);
        println!("(no) Ord. refraciton index:               {}", self.no);
        println!("(ne) Ext. refraciton index:               {}", self.ne);
        println!("(h) Etalon thickness [m]:                 {:+e}", self.h);
        println!("(r) Reflectivity:                         {}", self.r);
        println!("(a) Absorptance:                          {}", self.a);
        println!("(wvl) Peak wavelength [m]:                {:+e}", self.wvl);
        println!("(m) Order of the resonance peak:          {}", self.m);
        println!("(d_h) Thickness var. to tune to wvl0 [m]: {:+e}", self.d_h);
        println!("(tau) Transmittance:                      {}", self.tau);
        println!("(fin) Finesse:                            {}", self.fin);
        println!("(theta3) etalon optical axis [degree]:    {}", self.theta3);
        println!("(rp) pupil radius [m]:                    {}", self.rp);
        println!("(f) focal [m]:                            {}", self.f);
        println!("(tol) Tolerance:                          {:+e}", self.tol);
        println!("---------Integration and instrument parameters ----------");
        println!("(intr) Rho int. values (from,to,step):    {:?}", self.intr);
        println!("(intt) Theta int. values (from,to,step):  {:?}", self.intt);
        println!("---------------------------------------------------------");
    }
}

#[inline(always)]
fn deltao(e_p: &EtalonProp, wave: f64, theta: f64) -> f64 {
    // Calculates the ordinary retardance between two consecutive rays
    (4.0*PI*e_p.h/wave) * (e_p.no.powf(2.0)-1.0+theta.cos().powf(2.0)).sqrt() 
}

#[inline(always)]
fn deltae(e_p: &EtalonProp, wave: f64, theta: f64) -> f64 {
    //  Calculates the extraordinary retardance between two consecutive rays
    let n: f64 = (e_p.no + e_p.ne) / 2.0 ;
    let thetat: f64 = (theta.sin()/n).asin(); 
    let phi: f64 = (4.0*PI*e_p.h*n) * (e_p.no - e_p.ne) * (thetat-e_p.theta3).sin().powf(2.0) / 
        ( wave * (n.powf(2.0) - theta.sin().powf(2.0)).sqrt() );
    phi + deltao(e_p, wave, theta)
}

#[inline(always)]
fn h11(e_p: &EtalonProp, wave: f64, theta: f64 ) -> Complex<f64> {
    // Calculates the first diagonal element of the etalon Jones matrix.
    // It includes the absolute phase originated by the first pass in the Etalon:
    // exp(i*delta/2)
    let dto: f64 = deltao(e_p, wave, theta) ;
    // let j: Complex<f64> = Complex::<f64>::new(0.0, 1.0);
    let complexexp1: Complex<f64> = (- J * dto).exp();
    let complexexp2: Complex<f64> = (  J * dto/2.0).exp();

    ( e_p.tau.sqrt() / (1.0 - e_p.r) ) * 
        (1.0 - e_p.r * complexexp1) * complexexp2 / 
        (1.0 + e_p.fin * (dto / 2.0).sin().powf(2.0) ) 
}

#[inline(always)]
fn h22(e_p: &EtalonProp, wave: f64, theta: f64) -> Complex<f64> {
    // Calculates the second diagonal element of the etalon Jones matrixself.
    // It includes the absolute phase originated by the first pass in the Etalon:
    //     exp(i*delta/2)
    let dte: f64 = deltae(e_p, wave, theta) ;
    let complexexp1: Complex<f64> = (- J * dte).exp();
    let complexexp2: Complex<f64> = (  J * dte/2.0).exp();

    ( e_p.tau.sqrt() / (1.0 - e_p.r) ) * 
        (1.0 - e_p.r * complexexp1) * complexexp2 / 
        (1.0 + e_p.fin * (dte / 2.0).sin().powf(2.0) ) 
}

#[inline(always)]
fn thetap(x: f64, y: f64, xi: f64, eta: f64,f: f64) -> f64 {
    (f.powf(2.0) / ((x-xi).powf(2.0) + (y-eta).powf(2.0)+ f.powf(2.0))).sqrt().acos()
}

#[inline(always)]
fn h11pint(r:f64, theta:f64, e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64) -> Complex<f64> {
    // Real part of H11tildeprima
    let alpha: f64 = (xi - xi0) / e_p.f  ; // cosine director in x direction      
    let beta: f64 = (eta - eta0) / e_p.f ; // cosine director in y direction      
    let mut phip: f64 =  (( eta0 - r * theta.sin() ) / ( xi0 - r * theta.cos() ) ).atan() ;   
    if phip.is_nan() {phip = 0.0};  
    let k: f64 =  2.0 * PI / wvl ;                                                         
    let tp: f64 = thetap(r * theta.cos(),r * theta.sin(), xi0, eta0, e_p.f);         
    let h1: Complex<f64> = h11(e_p, wvl, tp ) ;                                      
    let h2: Complex<f64> = h22(e_p, wvl, tp ) ;                            

    // println!("Inside rust h11pint { }  { } { } { } { } { } { }", r, theta, xi, eta, xi0, eta0, wvl);
    // println!("------ alpha beta phip k tp h1 h2 { }  { } { } { } { } { } { }", alpha, beta, phip, k, tp, h1, h2);

    r * ( ( h1 * phip.cos().powf(2.0) + h2 * phip.sin().powf(2.0) ) *
        ( -J * k * (r * theta.cos() * alpha + r * theta.sin() * beta) ).exp() )

}

#[inline(always)]
fn simpsolve<F: Fn(f64,f64,&EtalonProp,f64,f64,f64,f64,f64) -> Complex<f64>>
    (startx: f64, endx: f64, mut stepsx: usize, starty: f64, endy: f64, mut stepsy: usize,
    e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64, 
    function: F,
) -> Complex<f64> {
    if stepsx & 1 == 1 {stepsx = stepsx + 1};
    if stepsy & 1 == 1 {stepsy = stepsy + 1};
    let stepx: f64 = (endx - startx) / stepsx as f64;
    let stepy: f64 = (endy - starty) / stepsy as f64;
    let mut result: Complex<f64> = Complex::<f64>::new(0.0, 0.0);

    let w : Vec<_> = (0..stepsy+1).into_iter().map(|i| wsipm1d(i,stepsx)).collect();
    for i in 0..stepsx+1 {
        for j in 0..stepsy+1 {
            result += function(startx + stepx * i as f64, starty + stepy * j as f64, e_p, xi, eta, xi0, eta0, wvl) * w[i] * w[j] ;
        }
    }

    // Standard loop way that works succesfully
    // let mut x = 0.0;
    // let mut y = 0.0;
    // for i in 0..stepsx+1 {
    //     x = startx + stepx * i as f64;
    //     for j in 0..stepsy+1 {
    //         y = starty + stepy * j as f64;
    //         result += function(x, y, e_p, xi, eta, xi0, eta0, wvl) *  wsipm2d(i,j,stepsx,stepsy) ;
    //     }
    // }

    // Trying using rayon iterators but its difficult (TBD)
    // let x : Vec<_> = (0..stepsx+1).into_iter().map(|i| startx + stepx * i as f64).collect();
    // let y : Vec<_> = (0..stepsy+1).into_iter().map(|i| starty + stepy * i as f64).collect();
    // let w : Vec<_> = (0..stepsy+1).into_iter().map(|i| wsipm(i,0,stepsx,stepsy)).collect();
    // x.into_iter().enumerate().map(|(i, xx)| {
    //     y.into_iter().enumerate().map(|(j, yy)| {
    //         result += function(xx, yy, e_p, xi, eta, xi0, eta0, wvl) *  wsipm(i,j,stepsx,stepsy) ;            
    //     });
    // });

    result * stepx * stepy / 9.0

}

fn wsipm2d(i: usize,j:usize, stepsx: usize, stepsy: usize) -> f64 {
    let mut weight: f64; 
    match i % 2 {
        0 => weight = 2.0,
        1 => weight = 4.0,
        _ => unreachable!(),
    }
    if (i == 0 || i == stepsx) && (j == 0 || j == stepsy) { weight = 1.0}
    else if i == 0 || i == stepsx {
        match j % 2 {
            0 => weight = 2.0,
            1 => weight = 4.0,
            _ => unreachable!(),
        }        
    } else if j == 0 || j == stepsy {
        match i % 2 {
            0 => weight = 2.0,
            1 => weight = 4.0,
            _ => unreachable!(),
        }        
    } else {
        match j % 2 {
            0 => weight *= 2.0,
            1 => weight *= 4.0,
            _ => unreachable!(),
        }        
    }
    // println!("{ } { } { } { } { }", i,j,weight, x, y);
    weight
}

#[inline(always)]
fn wsipm1d(i: usize, stepsx: usize) -> f64 {
    let weight: f64; 
    if i == 0 || i == stepsx { weight = 1.0}
    else {
    match i % 2 {
        0 => weight = 2.0,
        1 => weight = 4.0,
        _ => unreachable!(),
        }
    }
    weight
}

#[pyfunction]
fn integrate(e_p: &EtalonProp, waveaxis: Vec<f64>, x:f64, y:f64, tiltx:f64, tilty:f64, teldegree:f64) -> Vec<f64> { //Vec<Complex<f64>> {//Vec<f64> {

    // def transm_fdt(x,y,wvl,tiltx=0,tilty=0,teldegree=0.23):
    // etalon_pars: etalon
    // x,y: relative coordinates of detector (from -1 to +1; 0,0 at center)
    // wvl: vector containing the wavelength sampling (etalon tuned at 617.3nm)
        // tiltx,tilty: tilt of the etalon in degree (0 by default)
        // teldegree: degree of telecentrism center-to-border in degree (0.23º by def.)

    let startx: f64 = e_p.intr[0] ;
    let endx: f64 = e_p.intr[1] ;
    let stepsx: usize = e_p.intr[2] as usize;
    let starty: f64 = e_p.intt[0];
    let endy: f64 = e_p.intt[1];
    let stepsy: usize = e_p.intt[2] as usize;

    let theta0x: f64 = tiltx * PI / 180.0;   //Chief ray angle incidence in X direction at etalon center
    let theta0y: f64 = tilty * PI / 180.0;   //Chief ray angle incidence in Y direction at etalon center
    let theta_tel: f64 = teldegree * PI / 180.0; //Nominal degree of telecentrism center-border

    // Coordinates
    let xi0 = e_p.f * theta0x;
    let eta0 = e_p.f * theta0y;
    let xi_lim = e_p.f * theta_tel; // FoV [m]
    let xi = x * xi_lim+xi0;
    let eta = y * xi_lim+eta0;

    // println!("stepsss { } { } { } { } { } { } ", startx,stepsx,endx,starty,stepsy,endy);
    // println!("inputt { } { } { } { } { } { } { } { }", xi,eta,xi,eta,e_p.f,2.0 * PI / waveaxis[1],waveaxis[1],e_p.theta3);

    // println!("rust h11pint { }", h11pint(0.004, PI/2.0, e_p, xi, eta, xi, eta, waveaxis[1]));

    // println!("wave {:?}", waveaxis);

    // [0.0,0.0].to_vec() 


    let result: Vec<Complex<f64>> = waveaxis.into_par_iter().map(|wave| {
        simpsolve(startx, endx, stepsx, starty, endy, stepsy, 
            e_p, xi, eta, xi, eta, wave, h11pint) / ( PI * e_p.rp.powf(2.0) )
    })
    .collect(); 

    // for i in 0..result.len() {
    //     println!("{:?}",result[i]);
    // }

    // create the output
    // let mut output: Vec<f64> = Vec::with_capacity(result.len());

    // for _i in 0..result.len() {
    //     output.push(1.0);
    // }

    // println!("******** result *** {:?}", result.len());
    // println!("******** output *** {:?}", output.len());

    // for (i, x) in waveaxis.iter().enumerate() {
    //     println!("In position {} we have value {}", i, x);
    // }

    // for i in 0..(result.len()-1) {
    //     output[i] = (result[i] * result[i].conj()).powf(2.0).re ;
    // }

    // x.par_iter().enumerate().for_each(|(index, val)| {
        //     println!("{} {}", val, index);
        // });

    // let dd: Vec<f64> = result.iter().map(|x| (x * x.conj()).powf(2.0).re).collect();
    // println!("******** output *** {:?}", dd.len());

    result.into_iter().map(|x| (x * x.conj()).re).collect()
        // output

}



// Rust has Iterator::map, so you can:

// some_vec.iter().map(|x| /* do something here */)
// However, Iterators are lazy so this won't do anything by itself. You can tack a .collect() onto the end to make a new vector with the new elements, if that's what you want:

// let some_vec = vec![1, 2, 3];
// let doubled: Vec<_> = some_vec.iter().map(|x| x * 2).collect();
// println!("{:?}", doubled);
// The standard way to perform side effects is to use a for loop:

// let some_vec = vec![1, 2, 3];
// for i in &some_vec {
//     println!("{}", i);
// }
// If the side effect should modify the values in place, you can use an iterator of mutable references:

// let mut some_vec = vec![1, 2, 3];
// for i in &mut some_vec {
//     *i *= 2;
// }
// println!("{:?}", some_vec); // [2, 4, 6]
// If you really want the functional style, you can use the .for_each() method:

// let mut some_vec = vec![1, 2, 3];
// some_vec.iter_mut().for_each(|i| *i *= 2);
// println!("{:?}", some_vec); // [2, 4, 6]

// fn integrate_parellel(e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64, theta3:f64) -> Vec<f64> {

//     let startx: f64 = 0.0 ;
//     let endx: f64 = e_p.rp ;
//     let stepsx: usize = 10 ;
//     let starty: f64 = 0.0;
//     let endy: f64 = 2.0 * PI;
//     let stepsy: usize = 100;
//     let delta_1: f64 = -60e-12;  //Lower boundary of the wavelength range
//     let delta_2: f64 = 60e-12;   //Upper boundary of the wavelength range
//     let nl: usize = 100;           //Number of wavelengths for the sampling of the profiles
//     let step: f64 = (delta_2 - delta_1) / nl as f64;  //

//     let num_threads = num_cpus::get() - 1 ;
//     println!("Number of threads { }",num_threads);

//     // Split the image into equal-sized chunks for each thread
//     let chunk_size = nl / num_threads;
//     let mut chunks = Vec::with_capacity(num_threads);
//     for i in 0..num_threads {
//         let start = i * chunk_size;
//         let end = if i == num_threads - 1 {
//             wvl + delta_2
//         } else {
//             wvl + delta_1 + chunk_size as f64 * step
//         };
//         chunks.push((start, end));
//     }
//     // Spawn threads to process each chunk of the image in parallel
//     let mut threads = Vec::with_capacity(num_threads);
//     let mut transmission = Vec::with_capacity(nl);
//     for (start, end) in chunks {

//         let mut threads = Vec::with_capacity(num_threads);

//         let mut output_chunk = Vec::with_capacity(nl);

//         let thread_handle = thread::spawn(move || {
//             process_chunk(start, end, &mut output_chunk);
//             (start..end).into_par_iter().map(|i| {
//                 simpson_integral(startx, endx, stepsx, starty, endy,stepsy, 
//                     e_p, xi, eta, xi0, eta0, wvl + delta_1 + step * i as f64, theta3, h11pintr)
//             })
//             .collect()        
//             });
//         threads.push(thread_handle);
//         }

//     // Wait for all threads to finish
//     for thread_handle in threads {
//         thread_handle.join().unwrap();
//     }
//     transmission
// }
 

/// A Python module implemented in Rust.
#[pymodule]
fn spg_etalon(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<EtalonProp>()?;
    m.add_function(wrap_pyfunction!(integrate, m)?)?;
    Ok(())
} 

// Run cargo test :)
#[cfg(test)]
mod tests {

    use super::*;
    const EPSILON: f64 = 1e-13;

    fn almost_equal(a: f64, b: f64, eps: f64) -> bool {
        (a - b).abs() < eps
    }
    #[test]
    fn test() {
        assert!(almost_equal(1.0, 1.0, EPSILON));
    }
}

