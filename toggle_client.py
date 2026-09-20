import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

STARTUP_DELAY_SEC = 3.0  


class ToggleClient(Node):
    def __init__(self):
        super().__init__('toggle_client')
        self.client = self.create_client(SetBool, 'toggle_movement')

        self.get_logger().info(
            f'Waiting {STARTUP_DELAY_SEC}s before calling toggle_movement service...'
        )
        self.delay_timer = self.create_timer(STARTUP_DELAY_SEC, self.call_service)

    def call_service(self):
        self.delay_timer.cancel()  

        if not self.client.wait_for_service(timeout_sec=5.0):
            self.get_logger().error('Service toggle_movement not available.')
            return

        request = SetBool.Request()
        request.data = True

        future = self.client.call_async(request)
        future.add_done_callback(self.service_response_callback)

    def service_response_callback(self, future):
        try:
            response = future.result()
            self.get_logger().info(
                f'Service call result: success={response.success}, message="{response.message}"'
            )
        except Exception as e:
            self.get_logger().error(f'Service call failed: {e}')


def main(args=None):
    rclpy.init(args=args)
    node = ToggleClient()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()