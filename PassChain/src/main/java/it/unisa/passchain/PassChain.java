package it.unisa.passchain;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.image.Image;
import javafx.stage.Stage;

import java.io.IOException;

public class PassChain extends Application {

    @Override
    public void start(Stage stage) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(getClass().getResource("fxml/authentication.fxml"));

        Scene scene = new Scene(fxmlLoader.load());
        stage.setTitle("Unlocker IoT");
        stage.setScene(scene);
        stage.setResizable(false);
        stage.getIcons().add(new Image("D:\\Progetti GitHub\\Progetto-IoT\\PassChain\\src\\main\\resources\\it\\unisa\\passchain\\assets\\icon.png"));
        stage.show();
    }

    public static void main(String[] args) {
        launch();
    }
}