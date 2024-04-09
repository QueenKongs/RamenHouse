// Copyright Epic Games, Inc. All Rights Reserved.

using UnrealBuildTool;

public class RamenHouse : ModuleRules
{
	public RamenHouse(ReadOnlyTargetRules Target) : base(Target)
	{
		PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

		PublicDependencyModuleNames.AddRange(new string[] { "Core", "CoreUObject", "Engine", "InputCore", "EnhancedInput" });
	}
}
