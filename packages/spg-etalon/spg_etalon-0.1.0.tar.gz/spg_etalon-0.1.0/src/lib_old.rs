use pyo3::prelude::*;
use num_complex::Complex;
use rayon::prelude::*;
use std::thread;
use std::sync::mpsc;
extern crate num_cpus;

pub const PI: f64 = 3.14159265358979323846264338327950288f64; // 3.14159274f64

#[pyclass]
pub struct EtalonProp { /// Etalon basic parameters
//   #[pyo3(get, set)]
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
        EtalonProp { wvl0, fnum , no, ne, h, r, a, wvl, m, d_h, tau, fin, rp, f, tol} 
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
        Ok(())
    }
    #[setter]
    fn set_f(&mut self, value: f64) -> PyResult<()> {
        self.f = value;
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
    // #[getter]
    // fn get_wvl0(&self) -> PyResult<f64> {
    //     Ok(self.wvl0)
    // }
    pub fn show(&self) {
        println!("---------------------------------------------------------");
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
        println!("(rp) pupil radius [m]:                    {}", self.rp);
        println!("(f) focal [m]:                            {}", self.f);
        println!("(tol) Tolerance:                          {:+e}", self.tol);
        println!("---------------------------------------------------------");
    }
}

// #[pyfunction]
fn deltao(e_p: &EtalonProp, wave: &f64, theta: &f64) -> f64 {
    // Calculates the ordinary retardance between two consecutive rays
    (4.0*PI*e_p.h/wave) * (e_p.no.powf(2.0)-1.0+theta.cos().powf(2.0)).sqrt() 
}

// #[pyfunction]
// fn deltao(e_p: &EtalonProp, wave: f64, theta: f64) -> PyResult<f64> {
//     // Calculates the ordinary retardance between two consecutive rays
//     Ok(_deltao(e_p, wave, theta ) ) 
// }

// #[pyfunction]
fn deltae(e_p: &EtalonProp, wave: &f64, theta: &f64, theta3: &f64 ) -> f64 {
    //  Calculates the extraordinary retardance between two consecutive rays
    let n: f64 = (e_p.no + e_p.ne) / 2.0 ;
    let thetat: f64 = (theta.sin()/n).asin(); 
    let phi: f64 = (4.0*PI*e_p.h*n) * (e_p.no - e_p.ne) * (thetat-theta3).sin().powf(2.0) / 
        ( wave * (n.powf(2.0) - theta.sin().powf(2.0)).sqrt() );
    phi + deltao(e_p, wave, theta)
}

// #[pyfunction]
fn h11(e_p: &EtalonProp, wave: &f64, theta: &f64 ) -> Complex<f64> {
    // Calculates the first diagonal element of the etalon Jones matrix.
    // It includes the absolute phase originated by the first pass in the Etalon:
    // exp(i*delta/2)
    let dto: f64 = deltao(e_p, &wave, &theta) ;
    let j: Complex<f64> = Complex::<f64>::new(0.0, 1.0);
    let complexexp1: Complex<f64> = (- j * dto).exp();
    let complexexp2: Complex<f64> = (  j * dto/2.0).exp();

    ( e_p.tau.sqrt() / (1.0 - e_p.r) ) * 
        (1.0 - e_p.r * complexexp1) * complexexp2 / 
        (1.0 + e_p.fin * (dto / 2.0).sin().powf(2.0) ) 
}

// #[pyfunction]
fn h22(e_p: &EtalonProp, wave: &f64, theta: &f64, theta3: &f64 ) -> Complex<f64> {
    // Calculates the second diagonal element of the etalon Jones matrixself.
    // It includes the absolute phase originated by the first pass in the Etalon:
    //     exp(i*delta/2)
    let dte: f64 = deltae(e_p, &wave, &theta, &theta3) ;
    let j: Complex<f64> = Complex::<f64>::new(0.0, 1.0);
    let complexexp1: Complex<f64> = (- j * dte).exp();
    let complexexp2: Complex<f64> = (  j * dte/2.0).exp();

    ( e_p.tau.sqrt() / (1.0 - e_p.r) ) * 
        (1.0 - e_p.r * complexexp1) * complexexp2 / 
        (1.0 + e_p.fin * (dte / 2.0).sin().powf(2.0) ) 
}

fn thetap(x: f64, y: f64, xi: f64, eta: f64,f: f64) -> f64 {
    (f.powf(2.0) / ((x-xi).powf(2.0) + (y-eta).powf(2.0)+ f.powf(2.0))).sqrt().acos()
}

// #[pyfunction]
fn h11pintr(r:f64, theta:f64, e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64, theta3:f64) -> f64 {
    // Real part of H11tildeprima
    let alpha: f64 = (xi - xi0) / e_p.f  ; // cosine director in x direction
    let beta: f64 = (eta - eta0) / e_p.f ; // cosine director in y direction
    let mut phip: f64 =  (( eta0 - r * theta.sin() ) / ( xi0 - r * theta.cos() ) ).atan() ;
    if phip.is_nan() {phip = 0.0};  
    let k: f64 =  2.0 * PI / wvl ;
    let tp: f64 = thetap(r * theta.cos(),r * theta.sin(), xi0, eta0, e_p.f);
    // println!("phip: { }, tp: { }",phip, tp);
    let h1: Complex<f64> = h11(e_p, &wvl, &tp ) ;
    let h2: Complex<f64> = h22(e_p, &wvl, &tp, &theta3 ) ;
    let j: Complex<f64> = Complex::<f64>::new(0.0, 1.0);

    // println!("ru {:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}", r,theta,xi,eta,xi0,eta0,k,e_p.f,wvl,theta3,alpha,beta);
    // println!("ru {:+e} {:+e} {:+e} {:+e}",wvl, xi0, eta0, e_p.f);
    
    r * ( ( h1 * phip.cos().powf(2.0) + h2 * phip.sin().powf(2.0) ) *
        ( -j * k * (r * theta.cos() * alpha + r * theta.sin() * beta) ).exp() ).re
}

// #[pyfunction]
fn h11pinti(r:f64, theta:f64, e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64, theta3:f64) -> f64 {
    // Real part of H11tildeprima
    let alpha: f64 = (xi - xi0) / e_p.f  ; // cosine director in x direction
    let beta: f64 = (eta - eta0) / e_p.f ; // cosine director in y direction
    let mut phip: f64 =  (( eta0 - r * theta.sin() ) / ( xi0 - r * theta.cos() ) ).atan() ;
    if phip.is_nan() {phip = 0.0};  
    let k: f64 =  2.0 * PI / wvl ;
    let tp: f64 = thetap(r * theta.cos(),r * theta.sin(), xi0, eta0, e_p.f);
    let h1: Complex<f64> = h11(e_p, &wvl, &tp ) ;
    let h2: Complex<f64> = h22(e_p, &wvl, &tp, &theta3 ) ;
    let j: Complex<f64> = Complex::<f64>::new(0.0, 1.0);

    // println!("ru {:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}{:+e}", r,theta,xi,eta,xi0,eta0,k,e_p.f,wvl,theta3,alpha,beta);
    // println!("ru {:+e} {:+e} {:+e} {:+e}",wvl, xi0, eta0, e_p.f);
    
    r * ( ( h1 * phip.cos().powf(2.0) + h2 * phip.sin().powf(2.0) ) *
        ( -j * k * (r * theta.cos() * alpha + r * theta.sin() * beta) ).exp() ).im
}

// #[pyfunction]
fn h11pint(r:f64, theta:f64, e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64, theta3:f64) -> Complex<f64> {
    // Real part of H11tildeprima
    let alpha: f64 = (xi - xi0) / e_p.f  ; // cosine director in x direction      
    let beta: f64 = (eta - eta0) / e_p.f ; // cosine director in y direction      
    let mut phip: f64 =  (( eta0 - r * theta.sin() ) / ( xi0 - r * theta.cos() ) ).atan() ;   
    if phip.is_nan() {phip = 0.0};  
    let k: f64 =  2.0 * PI / wvl ;                                                         
    let tp: f64 = thetap(r * theta.cos(),r * theta.sin(), xi0, eta0, e_p.f);         
    let h1: Complex<f64> = h11(e_p, &wvl, &tp ) ;                                      
    let h2: Complex<f64> = h22(e_p, &wvl, &tp, &theta3 ) ;                            
    let j: Complex<f64> = Complex::<f64>::new(0.0, 1.0);

    r * ( ( h1 * phip.cos().powf(2.0) + h2 * phip.sin().powf(2.0) ) *
        ( -j * k * (r * theta.cos() * alpha + r * theta.sin() * beta) ).exp() )

}

fn simpson_integral<F: Fn(f64,f64,&EtalonProp,f64,f64,f64,f64,f64,f64) -> f64>
    (startx: f64, endx: f64, mut stepsx: usize, starty: f64, endy: f64, mut stepsy: usize,
    e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64, theta3:f64, 
    function: F,
) -> f64 {
    if stepsx%1 == 1 {stepsx = stepsx + 1};
    if stepsy%1 == 1 {stepsy = stepsy + 1};
    let stepx: f64 = (endx - startx) / stepsx as f64;
    let stepy: f64 = (endy - starty) / stepsy as f64;
    let mut result: f64 = 0.0;

    for i in 0..stepsx+1 {
        let x = startx + stepx * i as f64;
        for j in 0..stepsy+1 {
            let y = starty + stepy * j as f64;
            result += function(x, y, e_p, xi, eta, xi0, eta0, wvl, theta3) *  wsipm(i,j,stepsx,stepsy) ;
        }
    }
    result * stepx * stepy / 9.0

}

fn simpson_integral_complex<F: Fn(f64,f64,&EtalonProp,f64,f64,f64,f64,f64,f64) -> Complex<f64>>
    (startx: f64, endx: f64, mut stepsx: usize, starty: f64, endy: f64, mut stepsy: usize,
    e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64, theta3:f64, 
    function: F,
) -> Complex<f64> {
    if stepsx & 1 == 1 {stepsx = stepsx + 1};
    if stepsy & 1 == 1 {stepsy = stepsy + 1};
    let stepx: f64 = (endx - startx) / stepsx as f64;
    let stepy: f64 = (endy - starty) / stepsy as f64;
    let mut result: Complex<f64> = Complex::<f64>::new(0.0, 0.0);

    for i in 0..stepsx+1 {
        let x = startx + stepx * i as f64;
        for j in 0..stepsy+1 {
            let y = starty + stepy * j as f64;
            result += function(x, y, e_p, xi, eta, xi0, eta0, wvl, theta3) *  wsipm(i,j,stepsx,stepsy) ;
        }
    }
    result * stepx * stepy / 9.0
}

fn simpson_integral_complex_2<F: Fn(f64,f64,&EtalonProp,f64,f64,f64,f64,f64,f64) -> Complex<f64>>
    (startx: f64, endx: f64, mut stepsx: usize, starty: f64, endy: f64, mut stepsy: usize,
    e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, wvl:f64, theta3:f64, 
    function: F,
) -> f64 {
    if stepsx & 1 == 1 {stepsx = stepsx + 1};
    if stepsy & 1 == 1 {stepsy = stepsy + 1};
    let stepx: f64 = (endx - startx) / stepsx as f64;
    let stepy: f64 = (endy - starty) / stepsy as f64;
    let mut result: Complex<f64> = Complex::<f64>::new(0.0, 0.0);

    for i in 0..stepsx+1 {
        let x = startx + stepx * i as f64;
        for j in 0..stepsy+1 {
            let y = starty + stepy * j as f64;
            result += function(x, y, e_p, xi, eta, xi0, eta0, wvl, theta3) *  wsipm(i,j,stepsx,stepsy) ;
        }
    }
    (result.re + result.im) * stepx * stepy / 9.0
}

fn wsipm(i: usize,j:usize, stepsx: usize, stepsy: usize) -> f64 {
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

pub fn simpson_integration_2d<F: Fn(f64,f64) -> f64>(
    startx: f64,
    endx: f64,
    mut stepsx: u64,
    starty: f64,
    endy: f64,
    mut stepsy: u64,
    function: F,
) -> f64 {
    if stepsx & 1 == 1 {stepsx = stepsx + 1};
    if stepsy & 1 == 1 {stepsy = stepsy + 1};
    let stepx: f64 = (endx - startx) / stepsx as f64;
    let stepy: f64 = (endy - starty) / stepsy as f64;
    // let mut vec = vec![0; ((stepsx+1)*(stepsy+1)) as usize];
    let mut weight: f64; 
    let mut result: f64 = 0.0; 
    for i in 1..stepsx+2 {
        let x: f64 = startx + stepx * (i - 1) as f64;
        for j in 1..stepsy+2 {
            let y: f64 = starty + stepy * (j - 1) as f64;
            match i % 2 {
                0 => weight = 4.0,
                1 => weight = 2.0,
                _ => unreachable!(),
            }    
            if (i == 1 || i == stepsx + 1) && (j == 1 || j == stepsy + 1) {
                weight = 1.0;
            } else if i == 1 || i == stepsx + 1 {
                match j % 2 {
                    0 => weight = 4.0,
                    1 => weight = 2.0,
                    _ => unreachable!(),
                }        
            } else if j == 1 || j == stepsy + 1 {
                match i % 2 {
                    0 => weight = 4.0,
                    1 => weight = 2.0,
                    _ => unreachable!(),
                }        
            } else {
                match j % 2 {
                    0 => weight *= 4.0,
                    1 => weight *= 2.0,
                    _ => unreachable!(),
                }        
            }
            // vec[((i-1)*(stepsx+1) + (j-1)) as usize] = weight as u64 ;
            // println!("in: {} {} {} {}",i, j, ((i-1)*(stepsx+1) + j), weight);
            result += function(x,y)*weight ;
        }
    }
    result * stepx * stepy / 9.0 
    // println!("{:?}", vec);
    // println!("{:?}", result);
}

fn simpson_integration_dummy<F: Fn(f64,f64) -> f64>
    (startx: f64, endx: f64, mut stepsx: usize, starty: f64, endy: f64, mut stepsy: usize, 
    function: F,
) -> f64 {
    if stepsx & 1  == 1 {stepsx = stepsx + 1};
    if stepsy & 1  == 1 {stepsy = stepsy + 1};
    let stepx: f64 = (endx - startx) / stepsx as f64;
    let stepy: f64 = (endy - starty) / stepsy as f64;
    // let mut weight: f64; 
    let mut result: f64 = 0.0;
    println!("steps { } { }", stepsx,stepsy);

    for i in 0..stepsx+1 {
        let x = startx + stepx * i as f64;
        for j in 0..stepsy+1 {
            let y = starty + stepy * j as f64;
            result += function(x, y) *  wsipm(i,j,stepsx,stepsy) ;
        }
    }
    println!("Rrsult: { } ",result  * stepx * stepy / 9.0);
    println!("Expected: { } ", 20.0 * PI.powf(2.0));
    
    result * stepx * stepy / 9.0
}

// #[pyfunction]
fn integratec(e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, theta3:f64) -> Vec<Complex<f64>> {//Vec<f64> {
    let startx: f64 = 0.0 ;
    let endx: f64 = e_p.rp ;
    let stepsx: usize = 100 ;
    let starty: f64 = 0.0;
    let endy: f64 = 2.0 * PI;
    let stepsy: usize = 100;
    let delta_1: f64 = 60e-12;  //Lower boundary of the wavelength range
    let delta_2: f64 = 60e-12;   //Upper boundary of the wavelength range
    let nl: usize = 121;           //Number of wavelengths for the sampling of the profiles
    let step: f64 = (delta_2 + delta_1) / (nl - 1) as f64;  //

    let result: Vec<_> = (0..nl).into_iter().map(|i| {
        simpson_integral_complex(startx, endx, stepsx, starty, endy,stepsy, 
            e_p, xi, eta, xi0, eta0, e_p.wvl - delta_1 + step * i as f64, theta3, h11pint)
    })
    .collect();

    result
}

#[pyfunction]
fn integrate(e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, theta3:f64) -> Vec<f64> { //Vec<Complex<f64>> {//Vec<f64> {
    let startx: f64 = 0.0 ;
    let endx: f64 = e_p.rp ;
    let stepsx: usize = 100 ;
    let starty: f64 = 0.0;
    let endy: f64 = 2.0 * PI;
    let stepsy: usize = 100;
    let delta_1: f64 = 60e-12;  //Lower boundary of the wavelength range
    let delta_2: f64 = 60e-12;   //Upper boundary of the wavelength range
    let nl: usize = 121;           //Number of wavelengths for the sampling of the profiles
    let step: f64 = (delta_2 + delta_1) / (nl - 1) as f64;  //

    // let result: Vec<_> = (0..nl).into_iter().map(|i| {
    //     simpson_integral_complex(startx, endx, stepsx, starty, endy,stepsy, 
    //         e_p, xi, eta, xi0, eta0, e_p.wvl - delta_1 + step * i as f64, theta3, h11pint)
    // })
    // .collect();

    // result.into_iter().map( |i| (i.re + i.im) / ( PI * e_p.rp.powf(2.0) )).collect::<Vec<_>>() 

    (0..nl).into_par_iter().map(|i| {
        simpson_integral_complex_2(startx, endx, stepsx, starty, endy,stepsy, 
            e_p, xi, eta, xi0, eta0, e_p.wvl - delta_1 + step * i as f64, theta3, h11pint) / ( PI * e_p.rp.powf(2.0) )
    })
    .collect()

}

// #[pyfunction]
fn integrateh11pinti(e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, theta3:f64) -> Vec<f64> {
    let startx: f64 = 0.0 ;
    let endx: f64 = e_p.rp ;
    let stepsx: usize = 100 ;
    let starty: f64 = 0.0;
    let endy: f64 = 2.0 * PI;
    let stepsy: usize = 100;
    let delta_1: f64 = 60e-12;  //Lower boundary of the wavelength range
    let delta_2: f64 = 60e-12;   //Upper boundary of the wavelength range
    let nl: usize = 121;           //Number of wavelengths for the sampling of the profiles
    let step: f64 = (delta_2 + delta_1) / (nl - 1) as f64;  //

    // let wave = linspace::<f64>(wvl-delta_1,wvl+delta_2, nl); // wavelength vector
    // (0..nl).into_par_iter().for_each(|x| println!("{:?}", wvl-delta_1 + step * x as f64));

    (0..nl).into_par_iter().map(|i| {
        simpson_integral(startx, endx, stepsx, starty, endy,stepsy, 
            e_p, xi, eta, xi0, eta0, e_p.wvl0 - delta_1 + step * i as f64, theta3, h11pinti)
    })
    .collect()

    // H11t = (H11tr[0]+1j*H11ti[0]) / (np.pi*Rp**2)

    // let result: Vec<_> = (0..nl).into_par_iter().map(|i| {
    //     simpson_integral(startx, endx, stepsx, starty, endy,stepsy, 
    //         e_p, xi, eta, xi0, eta0, wvl - delta_1 + step * i as f64, theta3, h11pintr)
    // })
    // .collect();

    // result

    // let x = vec![5, 6, 7, 8];
    // x.par_iter().enumerate().for_each(|(index, val)| {
    //     println!("{} {}", val, index);
    // });
    

    // simpson_integral(startx, endx, stepsx, starty, endy,stepsy, e_p, xi, eta, xi0, eta0, wvl, theta3, h11pintr)
}

// #[pyfunction] 
fn integrateh11pintr(e_p: &EtalonProp, xi:f64, eta:f64, xi0:f64, eta0:f64, theta3:f64) -> Vec<f64> {
    let startx: f64 = 0.0 ;
    let endx: f64 = e_p.rp ;
    let stepsx: usize = 100 ;
    let starty: f64 = 0.0;
    let endy: f64 = 2.0 * PI;
    let stepsy: usize = 100;
    let delta_1: f64 = 60e-12;  //Lower boundary of the wavelength range
    let delta_2: f64 = 60e-12;   //Upper boundary of the wavelength range
    let nl: usize = 121;           //Number of wavelengths for the sampling of the profiles
    let step: f64 = (delta_1 + delta_2) / (nl - 1) as f64;  //
    // wvl0 = etm.wvl0 #Central wavelength (617.3 nm)
    // delta_1 = 60e-12 #Lower boundary of the wavelength range
    // delta_2 = 60e-12 #Upper boundary of the wavelength range
    // Nl = 6 #Number of wavelengths for the sampling of the profiles
    // wvlv = wvl0 + np.linspace(-delta_1, delta_2, Nl) #Wavelengths vector
    // lims = [[0,Rp],[0,2*np.pi]]
    
    // let wave = linspace::<f64>(wvl-delta_1,wvl+delta_2, nl); // wavelength vector
    // (0..nl).into_iter().for_each(|x| println!("Eje: {:?} {:?} {:?}", x, e_p.wvl0 - delta_1 + step * x as f64, - delta_1 + step * x as f64));

    (0..nl).into_par_iter().map(|i| {
        simpson_integral(startx, endx, stepsx, starty, endy,stepsy, 
            e_p, xi, eta, xi0, eta0, e_p.wvl0 - delta_1 + step * i as f64, theta3, h11pintr)
    })
    .collect()

    // H11t = (H11tr[0]+1j*H11ti[0]) / (np.pi*Rp**2)

    // let result: Vec<_> = (0..nl).into_par_iter().map(|i| {
    //     simpson_integral(startx, endx, stepsx, starty, endy,stepsy, 
    //         e_p, xi, eta, xi0, eta0, wvl - delta_1 + step * i as f64, theta3, h11pintr)
    // })
    // .collect();

    // result

    // let x = vec![5, 6, 7, 8];
    // x.par_iter().enumerate().for_each(|(index, val)| {
    //     println!("{} {}", val, index);
    // });
    

    // simpson_integral(startx, endx, stepsx, starty, endy,stepsy, e_p, xi, eta, xi0, eta0, wvl, theta3, h11pintr)
}


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
    // m.add_function(wrap_pyfunction!(deltao, m)?)?;
    // m.add_function(wrap_pyfunction!(deltae, m)?)?;
    // m.add_function(wrap_pyfunction!(h11, m)?)?;
    // m.add_function(wrap_pyfunction!(h22, m)?)?;
    // m.add_function(wrap_pyfunction!(h11pinti, m)?)?;
    // m.add_function(wrap_pyfunction!(h11pintr, m)?)?;
    // m.add_function(wrap_pyfunction!(h11pint, m)?)?;
    // m.add_function(wrap_pyfunction!(integrateh11pinti, m)?)?;
    // m.add_function(wrap_pyfunction!(integrateh11pintr, m)?)?;
    // m.add_function(wrap_pyfunction!(integratec, m)?)?;
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
    fn simpson2d() {
        use std::f64::consts::PI;
        // Calculate area under f(x) = cos(x) + 5 for -pi <= x <= pi
        // cosine should cancel out and the answer should be 2pi * 5
        let function = |x: f64, y: f64| -> f64 { x.cos() + y.sin() + 5.0 };
        let result = simpson_integration_dummy(0.0, 2.0*PI, 6, 0.0, 2.0*PI, 6, function);
        let expected = 20.0 * PI.powf(2.0);
        assert!(almost_equal(result, expected, EPSILON));
    }

    #[test]
    fn simpson2dd() {
        use std::f64::consts::PI;
        // Calculate area under f(x) = cos(x) + 5 for -pi <= x <= pi
        // cosine should cancel out and the answer should be 2pi * 5
        let function = |x: f64, y: f64| -> f64 { x.cos() + y.sin() + 5.0 };
        let result = simpson_integration_2d(0.0, 2.0*PI, 6, 0.0, 2.0*PI, 6, function);
        let expected = 20.0 * PI.powf(2.0);
        assert!(almost_equal(result, expected, EPSILON));
    }
}

