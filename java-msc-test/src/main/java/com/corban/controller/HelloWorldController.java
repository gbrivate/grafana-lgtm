package com.corban.controller;

import com.corban.dto.UserDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class HelloWorldController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello";
    }

    @GetMapping("/slow")
    public ResponseEntity<String> slowEndpoint() throws InterruptedException {
        // Simulate latency between 500–1500 ms
        long delay = 500 + (long) (Math.random() * 1000);
        Thread.sleep(delay);

        return ResponseEntity.ok("Slept for " + delay + " ms");
    }

    @GetMapping("/loop")
    public String loop(@RequestParam long id) {
        long start = System.currentTimeMillis();
        long duration = 0;
        try {
            while (id > 0) {
                id--;
                Thread.sleep(20);
            }
            long end = System.currentTimeMillis();
            duration = end - start;
            duration = duration / 1000;
        } catch (Exception e) {

        }

        return "Process completed: " + duration;
    }

    @PostMapping("/user")
    public String test(@RequestBody UserDTO userDTO) {
        return "ok "+userDTO.getName();
    }
}
