use std::thread;
use image::{DynamicImage, GenericImageView, ImageBuffer, Rgba};

fn main() {
    // Load the input image
    let input_image = image::open("input.png").unwrap();

    // Create a new image buffer to store the output
    let mut output_image = ImageBuffer::new(input_image.width(), input_image.height());

    // Define the number of threads to use
    let num_threads = 4;

    // Split the image into equal-sized chunks for each thread
    let chunk_size = input_image.height() / num_threads;
    let mut chunks = Vec::with_capacity(num_threads);
    for i in 0..num_threads {
        let start = i * chunk_size;
        let end = if i == num_threads - 1 {
            input_image.height()
        } else {
            (i + 1) * chunk_size
        };
        chunks.push((start, end));
    }

    // Spawn threads to process each chunk of the image in parallel
    let mut threads = Vec::with_capacity(num_threads);
    for (start, end) in chunks {
        let input_chunk = input_image.clone().crop_imm(0, start, input_image.width(), end - start);
        let mut output_chunk = output_image.clone().crop_imm(0, start, input_image.width(), end - start);
        let thread_handle = thread::spawn(move || {
            process_chunk(&input_chunk, &mut output_chunk);
        });
        threads.push(thread_handle);
    }

    // Wait for all threads to finish
    for thread_handle in threads {
        thread_handle.join().unwrap();
    }

    // Save the output image
    output_image.save("output.png").unwrap();
}

fn process_chunk(input_chunk: &DynamicImage, output_chunk: &mut ImageBuffer<Rgba<u8>, Vec<u8>>) {
    for (x, y, pixel) in input_chunk.pixels() {
        let transformed_pixel = transform_pixel(pixel);
        output_chunk.put_pixel(x, y, transformed_pixel);
    }
}

fn transform_pixel(pixel: &Rgba<u8>) -> Rgba<u8> {
    // Perform some operation on the pixel here
    // For example, invert the color
    Rgba([255 - pixel[0], 255 - pixel[1], 255 - pixel[2], pixel[3]])
}
