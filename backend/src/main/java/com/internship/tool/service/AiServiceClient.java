package com.internship.tool.service;

import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.client.HttpClientErrorException;

import java.util.Map;

@Service
public class AiServiceClient {

    private final RestTemplate restTemplate;

    public AiServiceClient(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public String generateResponse(String prompt) {
        try {
            String url = System.getenv().getOrDefault(
                    "AI_SERVICE_URL",
                    "http://ai-service:5000"
            ) + "/ai/generate";

            System.out.println(" Calling AI at: " + url);

            Map<String, String> body = Map.of("prompt", prompt);

            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            HttpEntity<Map<String, String>> request =
                    new HttpEntity<>(body, headers);

            try {
                ResponseEntity<Map> response = restTemplate.exchange(
                        url,
                        HttpMethod.POST,
                        request,
                        Map.class
                );

                if (response.getStatusCode().is2xxSuccessful()
                        && response.getBody() != null) {

                    return response.getBody().get("response").toString();
                }

            } catch (HttpClientErrorException.TooManyRequests e) {
                System.out.println("⚠ Rate limit hit");
                return "Rate limit exceeded. Please try again later.";
            }

            System.out.println("AI Raw Response: " + response.getBody());

            return response.getBody();

        } 
    
        catch (HttpClientErrorException e) {

            String errorBody = e.getResponseBodyAsString();
            System.out.println("AI Client Error: " + errorBody);

            // return actual error from Flask (400 cases)
            return errorBody;
        } 
        catch (Exception e) {
            System.out.println("AI ERROR:");
            e.printStackTrace();
        }

        return null;
    }
}