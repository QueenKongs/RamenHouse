// Fill out your copyright notice in the Description page of Project Settings.

#pragma once

#include "CoreMinimal.h"
#include "Networking.h"
#include "Sockets.h"
#include "SocketSubsystem.h"
#include "SocketServer.generated.h"

UCLASS()
class RAMENHOUSE_API ASocketServer : public AActor
{
	GENERATED_BODY()
	
public:	
	// Sets default values for this actor's properties
	ASocketServer();

protected:
	// Called when the game starts or when spawned
	virtual void BeginPlay() override;


private:
	FSocket* ListenerSocket;
	FSocket* ConnectionSocket;
	FIPv4Endpoint RemoteAddress;

	void StartListening();
	void HandleConnection();
	void ReceiveData();
};
