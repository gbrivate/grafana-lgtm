package com.lgtm.controller;

import com.lgtm.dto.UserDTO;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.http.HttpStatus;

import java.util.Map;

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

    @GetMapping("/error")
    public ResponseEntity<?> errorByStatus(
        @RequestParam int status,
        @RequestParam(required = false, defaultValue = "Custom error") String message) {
            HttpStatus httpStatus;

            try {
                httpStatus = HttpStatus.valueOf(status);
            } catch (IllegalArgumentException ex) {
                return ResponseEntity
                        .status(HttpStatus.BAD_REQUEST)
                        .body(Map.of(
                                "error", "Invalid HTTP status code",
                                "status", status
                        ));
            }

            return ResponseEntity
                    .status(httpStatus)
                    .body(Map.of(
                            "error", message,
                            "status", httpStatus.value(),
                            "reason", httpStatus.getReasonPhrase()
                    ));
        }
}
