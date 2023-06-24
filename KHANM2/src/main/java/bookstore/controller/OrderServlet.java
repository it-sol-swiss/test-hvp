package bookstore.controller;

import bookstore.model.Order;
import bookstore.model.OrderService;
import jakarta.servlet.annotation.WebServlet;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;

import java.io.IOException;
import java.util.List;

@WebServlet(urlPatterns = "/api/orders/*")
public class OrderServlet extends HttpServlet {

    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response) throws IOException {
        String pathInfo = request.getPathInfo();

        if (pathInfo == null || pathInfo.equals("/")) {
            List<Order> orders = OrderService.getAllOrders();
            response.setContentType("application/json");
            response.getWriter().write(new ObjectMapper().writeValueAsString(orders));
        } else {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
        }
    }


    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // Extrahieren der Bestellungsdetails aus dem Anforderungskörper
        Order order = new ObjectMapper().readValue(request.getReader(), Order.class);

        // Erstellen der Bestellung
        OrderService.createOrder(order);

        // Senden der Erfolgsantwort
        response.setStatus(HttpServletResponse.SC_CREATED);
        response.getWriter().write("Order created successfully.");
    }


    @Override
    protected void doDelete(HttpServletRequest request, HttpServletResponse response) throws IOException {
        // Extrahieren der Bestell-ID aus dem Pfad der Anforderung
        String pathInfo = request.getPathInfo();

        if (pathInfo == null || pathInfo.equals("/")) {
            response.setStatus(HttpServletResponse.SC_BAD_REQUEST);
            return;
        }

        String orderId = pathInfo.substring(1);

        // Löschen der Bestellung
        OrderService.deleteOrder(orderId);

        // Senden der Erfolgsantwort
        response.getWriter().write("Order deleted successfully.");
    }
}
