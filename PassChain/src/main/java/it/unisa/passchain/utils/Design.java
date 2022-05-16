package it.unisa.passchain.utils;

import javafx.animation.FadeTransition;
import javafx.animation.TranslateTransition;
import javafx.beans.value.ChangeListener;
import javafx.beans.value.ObservableValue;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.image.ImageView;
import javafx.scene.layout.AnchorPane;
import javafx.scene.text.Text;
import javafx.util.Duration;
import org.eclipse.paho.client.mqttv3.MqttException;

import java.net.UnknownHostException;

public class Design {

    public static void setSidebar(AnchorPane panel1, AnchorPane panel2, ImageView menu){
        panel1.setVisible(false);

        FadeTransition fadeTransition = new FadeTransition(Duration.seconds(0.4),panel1);
        fadeTransition.setFromValue(1);
        fadeTransition.setToValue(0);
        fadeTransition.play();

        TranslateTransition translateTransition = new TranslateTransition(Duration.seconds(0.4),panel2);
        translateTransition.setByX(-600);
        translateTransition.play();

        menu.setOnMouseClicked(event -> {
            panel1.setVisible(true);

            FadeTransition fadeTransition1 = new FadeTransition(Duration.seconds(0.4),panel1);
            fadeTransition1.setFromValue(0);
            fadeTransition1.setToValue(0.15);
            fadeTransition1.play();

            TranslateTransition translateTransition1 = new TranslateTransition(Duration.seconds(0.4),panel2);
            translateTransition1.setByX(+600);
            translateTransition1.play();
        });

        panel1.setOnMouseClicked(event -> {
            FadeTransition fadeTransition1 = new FadeTransition(Duration.seconds(0.4),panel1);
            fadeTransition1.setFromValue(0.15);
            fadeTransition1.setToValue(0);
            fadeTransition1.play();

            fadeTransition1.setOnFinished(event1 -> panel1.setVisible(false));

            TranslateTransition translateTransition1 = new TranslateTransition(Duration.seconds(0.4),panel2);
            translateTransition1.setByX(-600);
            translateTransition1.play();
        });
    }

    public static void setCredentials(TextField oldName, TextField webName, TextField username, TextField password) {
        if (oldName != null){
            oldName.setStyle("-fx-background-color: rgba(91, 155, 233, 0.78); " +
                    "-fx-text-fill: white; ");
            oldName.setPromptText("Old name Application");
        }

        if (webName != null){
            webName.setStyle("-fx-background-color: rgba(91, 155, 233, 0.78); " +
                    "-fx-text-fill: white; ");
            webName.setPromptText("Name Application");
        }

        if (username != null){
            username.setStyle("-fx-background-color: rgba(91, 155, 233, 0.78); " +

                    "-fx-text-fill: white; ");
            username.setPromptText("Username");
        }

        if (password != null){
            password.setStyle("-fx-background-color: rgba(91, 155, 233, 0.78); " +

                    "-fx-text-fill: white; ");
            password.setPromptText("Password");
        }
    }

    public static void textAreaNotEditable(TextArea txtArea) {
        txtArea.setEditable(false);
        txtArea.setFocusTraversable(false);
        txtArea.textProperty().addListener(new ChangeListener<Object>() {
            @Override
            public void changed(ObservableValue<?> observable, Object oldValue,
                                Object newValue) {
                txtArea.setScrollTop(Double.MAX_VALUE);
            }
        });
    }

    public static void fillTextArea(TextArea txtArea){
        CredentialsList credentialsList = new CredentialsList();
        txtArea.setText("");
        for (Credential c: credentialsList.getCredentials()) {
            txtArea.appendText("Nome: " + c.getName() + "\n");
            txtArea.appendText("Username: " + c.getUsername() + "\n");
            txtArea.appendText("Password: " + c.getPassword() + "\n\n");
        }
    }

    public static void connect(Text connected, Text notConnected) {
        if (MQTT_comunication.isConnected()) {
            connected.setText("Connessione PassChain riuscita.");
            connected.setOpacity(1);
            notConnected.setOpacity(0);
        }
        else {
            try {
                MQTT_comunication.connect();
            } catch (MqttException | UnknownHostException e) {
                throw new RuntimeException(e);
            }
            if (MQTT_comunication.isConnected()) {
                connected.setText("Connessione PassChain riuscita.");
                connected.setOpacity(1);
                notConnected.setOpacity(0);
            } else{
                notConnected.setText("ERROR: server MQTT.");
                connected.setOpacity(0);
                notConnected.setOpacity(1);
            }
        }
    }
}
