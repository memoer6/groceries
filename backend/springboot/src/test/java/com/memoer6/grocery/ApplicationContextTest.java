package com.memoer6.grocery;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

//The @SpringBootTest annotation tells Spring Boot to look for a main configuration class
// (one with @SpringBootApplication, for instance) and use that to start a Spring application context. You can
// run this test in your IDE or on the command line (by running ./mvnw test or ./gradlew test), and it should pass.

// Simple sanity check test that will fail if the application context cannot start
@SpringBootTest
public class ApplicationContextTest {
    @Test
    public void contextLoads() {
    }
}
