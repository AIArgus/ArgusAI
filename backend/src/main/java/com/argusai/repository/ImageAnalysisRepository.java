package com.argusai.repository;

import com.argusai.model.ImageAnalysis;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ImageAnalysisRepository extends JpaRepository<ImageAnalysis, Long> {
} 