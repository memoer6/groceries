package com.memoer6.grocery;



import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;


//Although it is possible to package this service as a traditional WAR file for deployment to an external application server,
//the simpler approach demonstrated below creates a standalone application. You package everything in a single, executable
// JAR file, driven by a good old Java main() method. Along the way, you use Spring’s support for embedding the Tomcat
// servlet container as the HTTP runtime, instead of deploying to an external instance.

@SpringBootApplication
public class Application {

    //Our main method delegates to Spring Boot’s SpringApplication class by calling run. SpringApplication will
    //bootstrap our application, starting Spring which will in turn start the auto-configured Tomcat web server. We need
    //to pass Application.class as an argument to the run method to tell SpringApplication which is the primary Spring component.
    //The args array is also passed through to expose any command-line arguments.
    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);

    }
}

//@SpringBootApplication is a convenience annotation that adds all of the following:
//-  @Configuration tags the class as a source of bean definitions for the application context.
//-  @EnableAutoConfiguration tells Spring Boot to start adding beans based on classpath settings, other beans, and
//    various property settings. By default all packages below your main configuration class (the one annotated with
//     @EnableAutoConfiguration or @SpringBootApplication) will be searched.
//-  Normally you would add @EnableWebMvc for a Spring MVC app, but Spring Boot adds it automatically when it sees
//spring-webmvc on the classpath. This flags the application as a web application and activates key behaviors
//such as setting up a DispatcherServlet.
//-  @ComponentScan tells Spring to look for other components, configurations, and services in the package, allowing
//it to find the UserController. Spring will scan the project's classpath looking for components, and make them available
//as autowire candidates within the application.


