package com.argusai.service;

import com.argusai.model.ImageAnalysis;
import com.argusai.repository.ImageAnalysisRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.time.LocalDateTime;
import java.util.Arrays;
import java.util.List;
import java.util.Random;

@Service
public class ImageAnalysisService {

    @Autowired
    private ImageAnalysisRepository repository;

    private final Random random = new Random();
    private final List<String> demoObjects = Arrays.asList(
        "telefon", "laptop", "książka", "kubek", "okulary", "klucze", "portfel", "długopis"
    );

    public ImageAnalysis analyzeImage(MultipartFile file, String analysisType, String targetObject) {
        ImageAnalysis analysis = new ImageAnalysis();
        analysis.setFileName(file.getOriginalFilename());
        analysis.setAnalysisType(analysisType);
        analysis.setTargetObject(targetObject);
        analysis.setCreatedAt(LocalDateTime.now());

        if ("OBJECT_DETECTION".equals(analysisType)) {
            // Demo response for object detection
            boolean found = random.nextBoolean();
            analysis.setResult(found ? 
                String.format("Znaleziono %d sztuk przedmiotu '%s' na zdjęciu.", 
                    random.nextInt(3) + 1, targetObject) :
                String.format("Nie znaleziono przedmiotu '%s' na zdjęciu.", targetObject));
        } else {
            // Demo response for general analysis
            int numObjects = random.nextInt(3) + 2;
            StringBuilder result = new StringBuilder("Na zdjęciu znaleziono następujące przedmioty:\n");
            for (int i = 0; i < numObjects; i++) {
                result.append("- ").append(demoObjects.get(random.nextInt(demoObjects.size()))).append("\n");
            }
            analysis.setResult(result.toString());
        }

        return repository.save(analysis);
    }
} 