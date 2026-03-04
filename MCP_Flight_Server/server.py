from mcp.server.fastmcp import FastMCP

# 1. 创建服务器实例
mcp = FastMCP("Flight Booking Server")

# 2. 静态资源 (Resources)：大模型可以读取的“字典”
@mcp.resource("file://airports")
def get_airports():
    """Get list of available airports"""
    return {
        "LAX": {"name": "Los Angeles International", "city": "Los Angeles"},
        "JFK": {"name": "John F. Kennedy International", "city": "New York"},
        "LHR": {"name": "London Heathrow", "city": "London"}
    }

# 3. 动作工具 (Tools)：大模型可以调用的“动作”
@mcp.tool()
def search_flights(origin: str, destination: str) -> dict:
    """Search for flights between two airports"""
    return {
        "flights": [
            {"id": "FL123", "origin": origin, "destination": destination, "price": 299},
            {"id": "FL456", "origin": origin, "destination": destination, "price": 399}
        ]
    }

@mcp.tool()
def create_booking(flight_id: str, passenger_name: str) -> dict:
    """Create a flight booking"""
    return {
        "booking_id": f"BK{flight_id[-3:]}",
        "flight_id": flight_id,
        "passenger": passenger_name,
        "status": "confirmed"
    }

# 4. 提示模板 (Prompts)：教大模型如何做事的“专家指导手册”
@mcp.prompt()
def find_best_flight(budget: float, preferences: str = "economy") -> str:
    """Generate a prompt for finding the best flight within budget"""
    return f"""Please help me find the best flight within a ${budget} budget.
My preferences: {preferences}
Use the search_flights tool to find available options and provide a recommendation with reasoning."""

if __name__ == "__main__":
    # 启动服务器，通过标准输入输出 (STDIO) 监听指令
    mcp.run()