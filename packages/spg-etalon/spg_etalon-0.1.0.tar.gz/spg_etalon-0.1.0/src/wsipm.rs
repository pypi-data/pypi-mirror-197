fn wsipm(i: usize,j:usize, stepsx: usize, stepsy: usize) -> f64 {
    let mut weight: f64; 
    if (i == 0 || i == stepsx) && (j == 0 || j == stepsy) {1.0}
    else if i == 0 || i == stepsx {
        match j % 2 {
            0 => 2.0,
            1 => 4.0,
            _ => unreachable!(),
        }        
    } else if j == 0 || j == stepsy {
        match i % 2 {
            0 => 2.0,
            1 => 4.0,
            _ => unreachable!(),
        }        
    } else {
        match i % 2 {
            0 => {
                match j % 2 {
                    0 => 4.0,
                    1 => 8.0,
                    _ => unreachable!(),
                }                
            },
            1 => {
                match j % 2 {
                    0 => 8.0,
                    1 => 16.0,
                    _ => unreachable!(),
                }                                
            },
            _ => unreachable!(),
        }
    }
    // println!("{ } { } { } { } { }", i,j,weight, x, y);
    weight
}