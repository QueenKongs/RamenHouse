#include "SocketServer.h"
#include "Sockets.h"

// Sets default values
ASocketServer::ASocketServer()
{
    // Set this actor to call Tick() every frame.  You can turn this off to improve performance if you don't need it.
    PrimaryActorTick.bCanEverTick = false;

    ListenerSocket = nullptr;
    ConnectionSocket = nullptr;
}

// Called when the game starts or when spawned
void ASocketServer::BeginPlay()
{
    Super::BeginPlay();
    StartListening();
}

void ASocketServer::StartListening()
{
    FIPv4Endpoint Endpoint(FIPv4Address::Any, 65432);
    ListenerSocket = FTcpSocketBuilder(TEXT("SocketListener"))
        .AsReusable()
        .BoundToEndpoint(Endpoint)
        .Listening(8);
    FTimerHandle DelayTimerHandle;
    GetWorldTimerManager().SetTimer(DelayTimerHandle, this, &ASocketServer::HandleConnection, 0.01, true);
}

void ASocketServer::HandleConnection()
{
    if (ListenerSocket == nullptr)
        return;

    if (ListenerSocket && ListenerSocket->HasPendingConnection())
    {
        ConnectionSocket = ListenerSocket->Accept(TEXT("Incoming connection"));
        if (ConnectionSocket != nullptr)
        {
            ReceiveData();
        }
    }
}

void ASocketServer::ReceiveData()
{
    FString ReceivedData;
    uint32 Size;
    while (ConnectionSocket->HasPendingData(Size))
    {
        ReceivedData.Empty(Size);
        int32 BytesRead = 0;
        ConnectionSocket->Recv((uint8*)TCHAR_TO_ANSI(*ReceivedData), Size, BytesRead);
        if (BytesRead > 0)
        {
            // ReceivedData¸¦ Ã³¸®
        }
    }
}