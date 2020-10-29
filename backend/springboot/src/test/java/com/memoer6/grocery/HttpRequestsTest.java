package com.memoer6.grocery;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;

// Note the use of webEnvironment=RANDOM_PORT to start the server with a random port (useful to avoid conflicts
// in test environments) and the injection of the port with @LocalServerPort. Also, note that Spring Boot has
// automatically provided a TestRestTemplate for you. All you have to do is add @Autowired to it.

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class HttpRequestsTest {

    @LocalServerPort
    private int port;

    @Autowired
    private TestRestTemplate restTemplate;

}
