package com.argusai.controller;

import com.argusai.model.ImageAnalysis;
import com.argusai.service.ImageAnalysisService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

@RestController
@RequestMapping("/api/analysis")
@CrossOrigin(origins = "http://localhost:3000")
public class ImageAnalysisController {

    @Autowired
    private ImageAnalysisService service;

    @PostMapping("/detect-object")
    public ResponseEntity<ImageAnalysis> detectObject(
            @RequestParam("file") MultipartFile file,
            @RequestParam("targetObject") String targetObject) {
        return ResponseEntity.ok(service.analyzeImage(file, "OBJECT_DETECTION", targetObject));
    }

    @PostMapping("/general-analysis")
    public ResponseEntity<ImageAnalysis> generalAnalysis(
            @RequestParam("file") MultipartFile file) {
        return ResponseEntity.ok(service.analyzeImage(file, "GENERAL_ANALYSIS", null));
    }
} 