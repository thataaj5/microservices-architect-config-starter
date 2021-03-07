FROM maven as build 
WORKDIR /app
COPY . .
RUN mvn install 

FROM openjdk:openjdk:11.0.10-jre
WORKDIR /app
COPY --from=build /app/target/offers-0.0.1-SNAPSHOT.jar /app
EXPOSE 9999
CMD ["java","-jar", "offers-0.0.1-SNAPSHOT.jar"]