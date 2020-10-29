package com.memoer6.grocery;

import com.memoer6.grocery.web.ProductController;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import static org.assertj.core.api.Assertions.assertThat;

//To convince yourself that the context is creating your controller, you could add an assertion,
// as the following example

@SpringBootTest
public class ControllerContextTest {

    @Autowired
    private ProductController controller;

    @Test
    public void contextLoads() throws Exception {
        assertThat(controller).isNotNull();
    }
}

//A nice feature of the Spring Test support is that the application context is cached between tests.
// That way, if you have multiple methods in a test case or multiple test cases with the same configuration,
// they incur the cost of starting the application only once. You can control the cache by using the
// @DirtiesContext annotation.
